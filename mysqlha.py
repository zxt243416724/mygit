#coding:utf-8
import  ConfigParser
import  string
import  commands
import  socket
import  fcntl
import  struct
from service import MySqlApp
from service import MySqlAppStatus



class  KeepalivedNode(object):

    filename="/etc/keepalived/keepalived.conf"
    def __init__(self,vip,real_server,priority):
        self.priority=priority
        self.str = """
              global_defs {
                    notification_email {
                    243416724@qq.com
                    }
                    notification_email_from 243416724@qq.com
                    smtp_server 127.0.0.1
                    smtp_connect_timeout 30
                    router_id MySQL-ha
                    }

               vrrp_instance VI_1 {
                    state BACKUP
                    interface eth0
                    virtual_router_id 51
                    priority %(priority)s
                    advert_int 1
                    authentication {
                    auth_type PASS
                    auth_pass 1111
                    }
                    virtual_ipaddress {
                     %(vip)s
                    }
                    }

               virtual_server %(vip)s 3306 {
                    delay_loop 2
                    lb_algo wrr
                    lb_kind DR
                    persistence_timeout 60
                    protocol TCP
                    real_server %(real_server)s 3306 {
                    weight 3
                    notify_down /etc/keepalived/MySQL.sh
                    TCP_CHECK {
                    connect_timeout 10
                    nb_get_retry 3
                    delay_before_retry 3
                    connect_port 3306
                    }
              }
              """ % {"priority":priority, "vip": vip, "real_server": real_server}

    def  update_config(self):
        os.system("mkdir  -p  /etc/keepalived/")
        f = open(KeepalivedNode.filename, "w")
        f.write(self.str)
        f.close()

"""
if __name__ == "__main__":
    node=KeepalivedNode("1.1.1.1","2.2.2.2")
    node.write_config()
"""

class MysqlHA(object):
    """
    xtzhang 2017-02-22 增加这个文件，实现修改mysql 的主主, 这个类的代码运行
    在guestagent里。
    """
    def __init__(self,cur_node_ip,partner_node_ip,vip,priority):
        """
        :param cur_node_ip:  本节点的ip
        :param partner_node_ip: 伙伴节点的ip (主主模式)
        :param vip: 虚拟ip,keepalived 提供
        :param priority: 优先级,keepalived 使用
        """
        self.cf = ConfigParser.ConfigParser(allow_no_value=True)
        #节点的IP地址 字典
        self.node_ip_dict={}
        if cur_node_ip is None:
           self.cur_node_ip=self.get_ip_address("eth0")
        else:
           self.cur_node_ip=cur_node_ip

        self.partner_node_ip=partner_node_ip
        #mysql 客户端操作对象
        self.app=MySqlApp(MySqlAppStatus.get())
        self.knode=KeepalivedNode(vip,cur_node_ip,priority)

    def get_ip_address(ifname):
        """
        获取本机eth0接口的ip 地址
        :return:
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', ifname[:15])
        )[20:24])

    def config_node_common(self,ipv4):
        #创建keepalived的目录
        (status, output) = commands.getstatusoutput('mkdir -p /etc/keepalived')
        self.knode.update_config()

        if self.node_ip_dict.has_key(ipv4):
            # 节点中已经存在指定IP 的节点
            return False
        ipseclist = string.split(ipv4, '.', 4)
        if len(ipseclist) != 4:
            # ip地址解析错误
            return False
        nodeid = ipseclist[3]

        # 打开二进制功能，主服务器必须打开
        self.cf.set("mysqld", "log-bin", "mysql-bin")
        self.cf.set("mysqld", "log_slave_updates", 1)

        # 忽略不同步主从的数据库
        self.cf.set("mysqld", "replicate-ignore-db", "mysql")
        self.cf.set("mysqld", "replicate-ignore-db", "information_schema")
        self.cf.set("mysqld", "replicate-ignore-db", "performance_schema")
        self.cf.set("mysqld", "replicate-ignore-db", "test")

        #取ip地址的最后个字段做MSYQL节点ID
        self.cf.set("mysqld", "server-id", nodeid)
        return  True

    def create_repl_user(self):
        """
        创建msyql 的复制用户
        """
        replication_user = {}
        replication_user['name'] = 'repl'
        replication_user['password'] = 'mysql'
        replication_user['host'] = self.partner_node_ip

        self.app.grant_replication_privilege(replication_user)

    def config_master_node_a(self):
        """
        MSYQL 主主配置MASTER-A节点
        #xtzhang  add

        log-bin=mysql-bin
        server-id=3
        log_slave_updates=1
        read_only=1
        """
        if  len(self.cur_node_ip)<=0:
            return False

        if  not self.config_node_common(self.cur_node_ip):
            return  False

        self.node_ip_dict[self.cur_node_ip] ="master-node-a"

        # 奇数id
        self.cf.set("auto_increment_offset",1)
        self.cf.set("auto_increment_increment", 2)

        self.create_repl_user()
        # 修改了mysql的配置后，需要重启数据库
        self.app.restart()

        return True

    def config_master_node_b(self):
        """
          MSYQL 主主配置MASTER-B节点
        """
        if not self.config_node_common(self.cur_node_ip):
            return False

        self.node_ip_dict[self.cur_node_ip] = "master-node-b"

        # 偶数id
        self.cf.set("auto_increment_offset", 2)
        self.cf.set("auto_increment_increment", 2)

        self.create_repl_user()
        # 修改了mysql的配置后，需要重启数据库
        self.app.restart()

        return True

    def create_node(self,log_file,position):
        """
        调用这个函数前需要先调用app.get_binlog_position 获取对端节点的日志文件位置
        :param log_file: 伙伴节点的复制日志文件
        :param position: 伙伴节点的复制起始位置 ( binlog_position=self.app.get_binlog_position())
        :return:
        """
        sql="""
        CHANGE
        MASTER
        TO
        MASTER_HOST = '%(partner_node_ip)s',
        MASTER_USER = 'repl',
        MASTER_PASSWORD = 'mysql',
        MASTER_LOG_FILE = '%(log_file)s',
        MASTER_LOG_POS = %(position)s;
        """  %  {"partner_node_ip":self.partner_node_ip,"log_file":log_file,"position":position}


        self.app.execute_on_client(sql)
        self.app.start_slave()
        self.app._get_slave_status()

        #重启keepalived
        (status, output) = commands.getstatusoutput('servcie keepalived  restart')



















