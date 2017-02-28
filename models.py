'''
Created on 2013/11/29

@author: zhanghaolun
'''

from trove.common import cfg

CONF = cfg.CONF

from trove.guestagent.db import models

class KSC_MySQLMasterStatus(models.Base):
    """Represents a MySQL Master status"""

    def __init__(self):
        self._file = None
        self._position = None
        self._binlog_do_db = None
        self._binlog_ignore_db = None

    def _is_valid(self, value):
        if value is None:
            return False
        else:
            return True

    @property
    def file(self):
        return self._file

    @file.setter
    def file(self, value):
        if not self._is_valid(value):
            raise ValueError("'%s' is not a valid file." % value)
        else:
            self._file = value

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        if not self._is_valid(value):
            raise ValueError("'%s' is not a valid position." % value)
        else:
            self._position = value

    @property
    def binlog_do_db(self):
        return self._binlog_do_db

    @binlog_do_db.setter
    def binlog_do_db(self, value):
        self._binlog_do_db = value

    @property
    def binlog_ignore_db(self):
        return self._binlog_ignore_db

    @binlog_ignore_db.setter
    def binlog_ignore_db(self, value):
        self._binlog_ignore_db = value



class KSC_MySQLSlaveStatus(models.Base):
    """Represents a MySQL Slave status"""

    def __init__(self):
        self.slave_io_state = None
        self.master_host = None
        self.master_user = None
        self.master_port = None
        self.connect_retry = None
        self.master_log_file = None
        self.read_master_log_pos = None
        self.relay_log_file = None
        self.replay_log_pos = None
        self.relay_master_log_file = None
        self.slave_io_running = None
        self.slave_sql_running = None
        self.replicate_do_db = None
        self.replicate_ignore_db = None
        self.replicate_do_table = None
        self.replicate_ignore_table = None
        self.replicate_wild_do_table = None
        self.replicate_wild_ignore_table = None
        self.last_errno = None
        self.last_error = None
        self.skip_counter = None

    def __str__(self):
        return str(self.__dict__)
        



class KSC_MySQLProcessInfo(models.Base):
    """Represents a MySQL Process info"""

    def __init__(self):
        self._id = None
        self._user = None
        self._host = None
        self._db = None
        self._command = None
        self._time = None
        self._state = None
        self._info = None

    def _is_valid(self, value):
        if value is None:
            return False
        else:
            return True

    @property
    def id(self):
        return self._file

    @id.setter
    def id(self, value):
        if not self._is_valid(value):
            raise ValueError("'%s' is not a valid id." % value)
        else:
            self._id = value

    @property
    def user(self):
        return self._position

    @user.setter
    def user(self, value):
        if not self._is_valid(value):
            raise ValueError("'%s' is not a valid user." % value)
        else:
            self._user = value

    @property
    def host(self):
        return self._host

    @host.setter
    def host(self, value):
        if not self._is_valid(value):
            raise ValueError("'%s' is not a valid host." % value)
        else:
            self._host = value

    @property
    def db(self):
        return self._db

    @db.setter
    def db(self, value):
        self._db = value

    @property
    def command(self):
        return self._command

    @command.setter
    def command(self, value):
        if not self._is_valid(value):
            raise ValueError("'%s' is not a valid command." % value)
        else:
            self._command = value

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, value):
        if not self._is_valid(value):
            raise ValueError("'%s' is not a valid time." % value)
        else:
            self._time = value

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        self._state = value

    @property
    def info(self):
        return self._info

    @info.setter
    def info(self, value):
        self._info = value


class KSC_BaseResultItem(models.Base):
    
#     SUPPORTED_ATTRIBUTES = ()
    
    def __init__(self):
        super(KSC_BaseResultItem, self).__init__()
        self._supported_variable_names = ()
    
    def __getattr__(self, name):
        if  name == '_supported_variable_names' or name.lower() in self._supported_variable_names:
            return self.__dict__.get(name.lower())
        else:
            raise ValueError('%s is not supported to get. ' % str(name))
    
    def __setattr__(self, k, v):
        
        if k == '_supported_variable_names' or k.lower() in self._supported_variable_names:
            self.__dict__[k.lower()] = v
        else:
            raise ValueError('%s is not supported to set. ' % str(k))
        
    def __len__(self):
        return self.__dict__.__len__()
    
    def serialize(self):
        r = {}
        for k, v in self.__dict__.items():
            if k == '_supported_variable_names':
                continue
            r[k] = v
            
        return r
    
    def deserialize(self, d):
        for k, v in d.items():
            self.__setattr__(k, v)


class KSC_MysqlSlaveStatusEx(KSC_BaseResultItem):
    SUPPORTED_ATTRIBUTES = (
        "connect_retry",
        "exec_master_log_pos",
        "last_errno",
        "last_error",
        "last_io_errno",
        "last_io_error",
        "last_sql_errno",
        "last_sql_error",
        "master_host",
        "master_log_file",
        "master_port",
        "master_server_id",
        "master_ssl_allowed",
        "master_ssl_ca_file",
        "master_ssl_ca_path",
        "master_ssl_cert",
        "master_ssl_cipher",
        "master_ssl_key",
        "master_ssl_verify_server_cert",
        "master_user",
        "read_master_log_pos",
        "relay_log_file",
        "relay_log_pos",
        "relay_log_space",
        "relay_master_log_file",
        "replicate_do_db",
        "replicate_do_table",
        "replicate_ignore_db",
        "replicate_ignore_server_ids",
        "replicate_ignore_table",
        "replicate_wild_do_table",
        "replicate_wild_ignore_table",
        "seconds_behind_master",
        "skip_counter",
        "slave_io_running",
        "slave_io_state",
        "slave_sql_running",
        "until_condition",
        "until_log_file",
        "until_log_pos",
    )
    
    def __init__(self):
        super(KSC_MysqlSlaveStatusEx, self).__init__()
        self._supported_variable_names = KSC_MysqlSlaveStatusEx.SUPPORTED_ATTRIBUTES
        
    def __cmp__(self, other):
#         if other == None:
#             raise ValueError("comparer is supported to be not None and instance of KSC_MysqlSlaveStatusEx, %s" % str(other))
        if None == other:
            return 1
        
        if (self.master_server_id == None or other.master_server_id == None or \
            self.master_server_id != other.master_server_id):
            raise ValueError("incorrect master server id, slave1: %s, slave2: %s" % (self.master_server_id, other.master_server_id))
        
        else:
            cmpResult = cmp(self.relay_master_log_file, other.relay_master_log_file)
            if cmpResult == 0:
                cmpResult = cmp(int(self.exec_master_log_pos), int(other.exec_master_log_pos))
            
            return cmpResult
    

class KSC_MySQLGlobalVariables(KSC_BaseResultItem):
    '''
    support variables descripted by http://dev.mysql.com/doc/refman/5.*/en/server-system-variables.html 
    
    '''
        
    SUPPORTED_VARIABLES = (
        "binlog_format",
        "datadir",
        "event_scheduler",
        "expire_logs_days",
        "log_bin",
        "max_binlog_size",
        "max_connections",  
        "innodb_max_dirty_pages_pct",
        "port",
        "read_only",
        "relay_log",
        "rpl_semi_sync_master_enabled",
        "rpl_semi_sync_slave_enabled",
        "rpl_semi_sync_master_timeout",
        "server_id",
        
        "innodb_file_per_table",
        "autocommit",
        "local_infile",
        "key_buffer_size",
        "connect_timeout",
        "join_buffer_size",
        "sort_buffer_size",
        "innodb_buffer_pool_size",
        "innodb_flush_log_at_trx_commit",
        "innodb_log_buffer_size",
        "innodb_open_files",
        "innodb_thread_concurrency",
        "innodb_additional_mem_pool_size",
        "sql_slave_skip_counter",
        "sync_binlog",
        "auto_increment_increment",
        "auto_increment_offset",
        "bulk_insert_buffer_size",
        "interactive_timeout",
        "max_allowed_packet",
        "max_connect_errors",
        "myisam_sort_buffer_size",
        "max_user_connections",
        "wait_timeout",
        "character_set_client",
        "character_set_connection",
        "character_set_database",
        "character_set_filesystem",
        "character_set_results",
        "character_set_server",
        "collation_connection",
        "collation_database",
        "collation_server",
        
        "log_bin_trust_function_creators",
        "lower_case_table_names",
        "query_cache_size",
        "query_cache_type",

        "open_files_limit",
        
        "long_query_time",
        "innodb_stats_on_metadata",
        "tx_isolation",
        "back_log",
        "concurrent_insert",
        "default_week_format",
        "delayed_insert_limit",
        "delayed_insert_timeout",
        "delayed_queue_size",
        "delay_key_write",
        "div_precision_increment",
        "ft_min_word_len",
        "ft_query_expansion_limit",
        "group_concat_max_len",
        "innodb_autoinc_lock_mode",
        "innodb_concurrency_tickets",
        "innodb_large_prefix",
        "innodb_lock_wait_timeout",
        "innodb_max_dirty_pages_pct",
        "innodb_old_blocks_pct",
        "innodb_old_blocks_time",
        "innodb_purge_batch_size",
        "innodb_purge_threads",
        "innodb_read_ahead_threshold",
        "innodb_read_io_threads",
        "innodb_rollback_on_timeout",
        "innodb_stats_method",
        "innodb_stats_sample_pages",
        "innodb_strict_mode",
        "innodb_table_locks",
        "innodb_thread_sleep_delay",
        "innodb_write_io_threads",
        "key_cache_age_threshold",
        "key_cache_block_size",
        "key_cache_division_limit",
        "log_queries_not_using_indexes",
        "low_priority_updates",
        "net_read_timeout",
        "net_retry_count",
        "net_write_timeout",
        "query_alloc_block_size",
        "query_cache_limit",
        "query_prealloc_size",
        "slow_launch_time",
        "table_definition_cache",
        "table_open_cache",
        "init_connect",
        "tmp_table_size"
    )
    
    def __init__(self):
        super(KSC_MySQLGlobalVariables, self).__init__()
        self._supported_variable_names = KSC_MySQLGlobalVariables.SUPPORTED_VARIABLES


class KSC_MysqlGlobalStatuses(KSC_BaseResultItem):
    
    SUPPORTED_STUTUS = (
        "com_delete", 
        "com_delete_multi",
        "com_insert", 
        "com_insert_multi",
        "com_update", 
        "com_update_multi",
        "com_select",
         
        "rpl_semi_sync_master_status",
        "rpl_semi_sync_slave_status",
        "rpl_semi_sync_master_no_tx",
        "rpl_semi_sync_master_yes_tx",
        
        "slave_running",
        "threads_cached",
        "threads_connected",
        "threads_running",

        "bytes_sent",
        "bytes_received",

        "innodb_data_fsyncs",
        "innodb_buffer_pool_pages_total",
        "innodb_buffer_pool_pages_data",
        "innodb_buffer_pool_pages_dirty",
        "innodb_data_read",
        "innodb_data_written",
        "innodb_buffer_pool_read_requests",
        "innodb_buffer_pool_reads",
        "innodb_page_size",

        "uptime",

        "aborted_connects",
        "max_used_connections",
        "connections",
        "slow_queries",

        "handler_delete",
        "handler_read_first",
        "handler_read_key",
        "handler_read_next",
        "handler_read_prev",
        "handler_read_rnd",
        "handler_read_rnd_next",
        "handler_write",
        "handler_update",

        "open_files"
    )
    
    def __init__(self):
        super(KSC_MysqlGlobalStatuses, self).__init__()
        self._supported_variable_names = KSC_MysqlGlobalStatuses.SUPPORTED_STUTUS

class KSC_MysqlSlaveHost(KSC_BaseResultItem):
    
    SUPPORTED_STUTUS = (
        "server_id",
        "host",
        "port",
        "master_id"
    )
    
    def __init__(self):
        super(KSC_MysqlSlaveHost, self).__init__()
        self._supported_variable_names = KSC_MysqlSlaveHost.SUPPORTED_STUTUS


class KSC_BinaryLogItem(KSC_BaseResultItem):
    
    SUPPORTED_VARIABLES = (
        "log_name",
        "file_size"
    )
    
    def __init__(self, log_name, file_size):
        super(KSC_BinaryLogItem, self).__init__()
        self._supported_variable_names = KSC_BinaryLogItem.SUPPORTED_VARIABLES
        self.log_name = log_name
        self.file_size = file_size
        
class KSC_BinlogItem(KSC_BaseResultItem):
    
    SUPPORTED_VARIABLES = (
        "log_name",
        "file_size",
        "start_time"
    )
    
    def __init__(self, log_name, file_size, start_time):
        super(KSC_BinlogItem, self).__init__()
        self._supported_variable_names = KSC_BinlogItem.SUPPORTED_VARIABLES
        self.log_name = log_name
        self.file_size = file_size
        self.start_time = start_time

class KSC_MySQLProcessInfoEx(KSC_BaseResultItem):
    SUPPORTED_VARIABLES = (
        "id", 
        "user", 
        "host", 
        "db", 
        "command", 
        "time", 
        "state", 
        "info",
    )

    def __init__(self):
        super(KSC_MySQLProcessInfoEx, self).__init__()
        self._supported_variable_names = KSC_MySQLProcessInfoEx.SUPPORTED_VARIABLES
        

class KSC_MySQLMasterStatusEx(KSC_BaseResultItem):
    """Represents a MySQL Master status"""
    SUPPORTED_VARIABLES = (
        "file",
        "position",
        "binlog_do_db",
        "binlog_ignore_db"
    )

    def __init__(self):
        super(KSC_MySQLMasterStatusEx, self).__init__()
        self._supported_variable_names = KSC_MySQLMasterStatusEx.SUPPORTED_VARIABLES


class KSC_TransactionStatus(KSC_BaseResultItem):

    SUPPORTED_STATUS = (
        "running",
        "lock_wait",
        "rolling_back",
        "committing"
    )

    def __init__(self):
        super(KSC_TransactionStatus, self).__init__()
        self._supported_variable_names = KSC_TransactionStatus.SUPPORTED_STATUS
