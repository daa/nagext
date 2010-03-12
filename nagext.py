"""
This module provides python interface to Nagios external commands
"""

from time import time

class ExecError(Exception):
    """
    Errors while executing command (writing external command to command file)
    """
    pass

class NagExt(object):
    """
    Deal with nagios command file for executing external commands.
    Writes commands to Nagios command_file in following format:
    [time] command_id;command_arguments

    """

    def __init__(self, command_file):
        self.command_file = command_file
        self._cmd_f = None
        self.open()
    
    def __del__(self):
        self.close()

    def open(self):
        """
        Open Nagios command file
        """
        self._cmd_f = open(self.command_file, 'w')
    
    def close(self):
        """
        Close Nagios command file
        """
        self._cmd_f.close()

    def run(self, cmd, *args):
    	"""
        Run Nagios external command with given arguments, converting bool to int
        """
        def bool2int(a):
            if isinstance(a, bool):
                return int(a)
            else:
                return a
        try:
            #str_args = ';'.join([ str(bool2int(a)) for a in args ])
            str_args = ';'.join(map(str, map(bool2int, args)))
            print >> self._cmd_f, "[%lu] %s;%s" % (time(), cmd, str_args)
        except Exception, e:
            raise ExecError(str(e))

    # next follow automatically generated methods from nagios developer documentation
    # for external commands

    def acknowledge_host_problem(self, host_name, sticky, notify, persistent, author, comment):
        """
        Allows you to acknowledge the current problem for the specified host.  By
        acknowledging the current problem, future notifications (for the same host
        state) are disabled.  If the "sticky" option is set to one (1), the
        acknowledgement will remain until the host returns to an UP state.  Otherwise
        the acknowledgement will automatically be removed when the host changes state.
        If the "notify" option is set to one (1), a notification will be sent out to
        contacts indicating that the current host problem has been acknowledged.  If the
        "persistent" option is set to one (1), the comment associated with the
        acknowledgement will survive across restarts of the Nagios process.  If not, the
        comment will be deleted the next time Nagios restarts.
        """
        self.run('ACKNOWLEDGE_HOST_PROBLEM', host_name, sticky, notify, persistent, author, comment)

    def acknowledge_svc_problem(self, host_name, service_description, sticky, notify, persistent, author, comment):
        """
        Allows you to acknowledge the current problem for the specified service.  By
        acknowledging the current problem, future notifications (for the same
        servicestate) are disabled.  If the "sticky" option is set to one (1), the
        acknowledgement will remain until the service returns to an OK state.  Otherwise
        the acknowledgement will automatically be removed when the service changes
        state.  If the "notify" option is set to one (1), a notification will be sent
        out to contacts indicating that the current service problem has been
        acknowledged.  If the "persistent" option is set to one (1), the comment
        associated with the acknowledgement will survive across restarts of the Nagios
        process.  If not, the comment will be deleted the next time Nagios restarts.
        """
        self.run('ACKNOWLEDGE_SVC_PROBLEM', host_name, service_description, sticky, notify, persistent, author, comment)

    def add_host_comment(self, host_name, persistent, author, comment):
        """
        Adds a comment to a particular host.  If the "persistent" field is set to zero
        (0), the comment will be deleted the next time Nagios is restarted.  Otherwise,
        the comment will persist across program restarts until it is deleted manually.
        """
        self.run('ADD_HOST_COMMENT', host_name, persistent, author, comment)

    def add_svc_comment(self, host_name, service_description, persistent, author, comment):
        """
        Adds a comment to a particular service.  If the "persistent" field is set to
        zero (0), the comment will be deleted the next time Nagios is restarted.
        Otherwise, the comment will persist across program restarts until it is deleted
        manually.
        """
        self.run('ADD_SVC_COMMENT', host_name, service_description, persistent, author, comment)

    def change_contact_host_notification_timeperiod(self, contact_name, notification_timeperiod):
        """
        Changes the host notification timeperiod for a particular contact to what is
        specified by the "notification_timeperiod" option.  The
        "notification_timeperiod" option should be the short name of the timeperiod that
        is to be used as the contact's host notification timeperiod.  The timeperiod
        must have been configured in Nagios before it was last (re)started.
        """
        self.run('CHANGE_CONTACT_HOST_NOTIFICATION_TIMEPERIOD', contact_name, notification_timeperiod)

    def change_contact_modattr(self, contact_name, value):
        """
        This command changes the modified attributes value for the specified contact.
        Modified attributes values are used by Nagios to determine which object
        properties should be retained across program restarts.  Thus, modifying the
        value of the attributes can affect data retention.  This is an advanced option
        and should only be used by people who are intimately familiar with the data
        retention logic in Nagios.
        """
        self.run('CHANGE_CONTACT_MODATTR', contact_name, value)

    def change_contact_modhattr(self, contact_name, value):
        """
        This command changes the modified host attributes value for the specified
        contact.  Modified attributes values are used by Nagios to determine which
        object properties should be retained across program restarts.  Thus, modifying
        the value of the attributes can affect data retention.  This is an advanced
        option and should only be used by people who are intimately familiar with the
        data retention logic in Nagios.
        """
        self.run('CHANGE_CONTACT_MODHATTR', contact_name, value)

    def change_contact_modsattr(self, contact_name, value):
        """
        This command changes the modified service attributes value for the specified
        contact.  Modified attributes values are used by Nagios to determine which
        object properties should be retained across program restarts.  Thus, modifying
        the value of the attributes can affect data retention.  This is an advanced
        option and should only be used by people who are intimately familiar with the
        data retention logic in Nagios.
        """
        self.run('CHANGE_CONTACT_MODSATTR', contact_name, value)

    def change_contact_svc_notification_timeperiod(self, contact_name, notification_timeperiod):
        """
        Changes the service notification timeperiod for a particular contact to what is
        specified by the "notification_timeperiod" option.  The
        "notification_timeperiod" option should be the short name of the timeperiod that
        is to be used as the contact's service notification timeperiod.  The timeperiod
        must have been configured in Nagios before it was last (re)started.
        """
        self.run('CHANGE_CONTACT_SVC_NOTIFICATION_TIMEPERIOD', contact_name, notification_timeperiod)

    def change_custom_contact_var(self, contact_name, varname, varvalue):
        """
        Changes the value of a custom contact variable.
        """
        self.run('CHANGE_CUSTOM_CONTACT_VAR', contact_name, varname, varvalue)

    def change_custom_host_var(self, host_name, varname, varvalue):
        """
        Changes the value of a custom host variable.
        """
        self.run('CHANGE_CUSTOM_HOST_VAR', host_name, varname, varvalue)

    def change_custom_svc_var(self, host_name, service_description, varname, varvalue):
        """
        Changes the value of a custom service variable.
        """
        self.run('CHANGE_CUSTOM_SVC_VAR', host_name, service_description, varname, varvalue)

    def change_global_host_event_handler(self, event_handler_command):
        """
        Changes the global host event handler command to be that specified by the
        "event_handler_command" option.  The "event_handler_command" option specifies
        the short name of the command that should be used as the new host event handler.
        The command must have been configured in Nagios before it was last (re)started.
        """
        self.run('CHANGE_GLOBAL_HOST_EVENT_HANDLER', event_handler_command)

    def change_global_svc_event_handler(self, event_handler_command):
        """
        Changes the global service event handler command to be that specified by the
        "event_handler_command" option.  The "event_handler_command" option specifies
        the short name of the command that should be used as the new service event
        handler.  The command must have been configured in Nagios before it was last
        (re)started.
        """
        self.run('CHANGE_GLOBAL_SVC_EVENT_HANDLER', event_handler_command)

    def change_host_check_command(self, host_name, check_command):
        """
        Changes the check command for a particular host to be that specified by the
        "check_command" option.  The "check_command" option specifies the short name of
        the command that should be used as the new host check command.  The command must
        have been configured in Nagios before it was last (re)started.
        """
        self.run('CHANGE_HOST_CHECK_COMMAND', host_name, check_command)

    def change_host_check_timeperiod(self, host_name, timeperiod):
        """
        Changes the valid check period for the specified host.
        """
        self.run('CHANGE_HOST_CHECK_TIMEPERIOD', host_name, timeperiod)

    def change_host_check_timeperiod(self, host_name, check_timeperod):
        """
        Changes the check timeperiod for a particular host to what is specified by the
        "check_timeperiod" option.  The "check_timeperiod" option should be the short
        name of the timeperod that is to be used as the host check timeperiod.  The
        timeperiod must have been configured in Nagios before it was last (re)started.
        """
        self.run('CHANGE_HOST_CHECK_TIMEPERIOD', host_name, check_timeperod)

    def change_host_event_handler(self, host_name, event_handler_command):
        """
        Changes the event handler command for a particular host to be that specified by
        the "event_handler_command" option.  The "event_handler_command" option
        specifies the short name of the command that should be used as the new host
        event handler.  The command must have been configured in Nagios before it was
        last (re)started.
        """
        self.run('CHANGE_HOST_EVENT_HANDLER', host_name, event_handler_command)

    def change_host_modattr(self, host_name, value):
        """
        This command changes the modified attributes value for the specified host.
        Modified attributes values are used by Nagios to determine which object
        properties should be retained across program restarts.  Thus, modifying the
        value of the attributes can affect data retention.  This is an advanced option
        and should only be used by people who are intimately familiar with the data
        retention logic in Nagios.
        """
        self.run('CHANGE_HOST_MODATTR', host_name, value)

    def change_max_host_check_attempts(self, host_name, check_attempts):
        """
        Changes the maximum number of check attempts (retries) for a particular host.
        """
        self.run('CHANGE_MAX_HOST_CHECK_ATTEMPTS', host_name, check_attempts)

    def change_max_svc_check_attempts(self, host_name, service_description, check_attempts):
        """
        Changes the maximum number of check attempts (retries) for a particular
        service.
        """
        self.run('CHANGE_MAX_SVC_CHECK_ATTEMPTS', host_name, service_description, check_attempts)

    def change_normal_host_check_interval(self, host_name, check_interval):
        """
        Changes the normal (regularly scheduled) check interval for a particular host.
        """
        self.run('CHANGE_NORMAL_HOST_CHECK_INTERVAL', host_name, check_interval)

    def change_normal_svc_check_interval(self, host_name, service_description, check_interval):
        """
        Changes the normal (regularly scheduled) check interval for a particular
        service
        """
        self.run('CHANGE_NORMAL_SVC_CHECK_INTERVAL', host_name, service_description, check_interval)

    def change_retry_host_check_interval(self, host_name, service_description, check_interval):
        """
        Changes the retry check interval for a particular host.
        """
        self.run('CHANGE_RETRY_HOST_CHECK_INTERVAL', host_name, service_description, check_interval)

    def change_retry_svc_check_interval(self, host_name, service_description, check_interval):
        """
        Changes the retry check interval for a particular service.
        """
        self.run('CHANGE_RETRY_SVC_CHECK_INTERVAL', host_name, service_description, check_interval)

    def change_svc_check_command(self, host_name, service_description, check_command):
        """
        Changes the check command for a particular service to be that specified by the
        "check_command" option.  The "check_command" option specifies the short name of
        the command that should be used as the new service check command.  The command
        must have been configured in Nagios before it was last (re)started.
        """
        self.run('CHANGE_SVC_CHECK_COMMAND', host_name, service_description, check_command)

    def change_svc_check_timeperiod(self, host_name, service_description, check_timeperiod):
        """
        Changes the check timeperiod for a particular service to what is specified by
        the "check_timeperiod" option.  The "check_timeperiod" option should be the
        short name of the timeperod that is to be used as the service check timeperiod.
        The timeperiod must have been configured in Nagios before it was last
        (re)started.
        """
        self.run('CHANGE_SVC_CHECK_TIMEPERIOD', host_name, service_description, check_timeperiod)

    def change_svc_event_handler(self, host_name, service_description, event_handler_command):
        """
        Changes the event handler command for a particular service to be that specified
        by the "event_handler_command" option.  The "event_handler_command" option
        specifies the short name of the command that should be used as the new service
        event handler.  The command must have been configured in Nagios before it was
        last (re)started.
        """
        self.run('CHANGE_SVC_EVENT_HANDLER', host_name, service_description, event_handler_command)

    def change_svc_modattr(self, host_name, service_description, value):
        """
        This command changes the modified attributes value for the specified service.
        Modified attributes values are used by Nagios to determine which object
        properties should be retained across program restarts.  Thus, modifying the
        value of the attributes can affect data retention.  This is an advanced option
        and should only be used by people who are intimately familiar with the data
        retention logic in Nagios.
        """
        self.run('CHANGE_SVC_MODATTR', host_name, service_description, value)

    def change_svc_notification_timeperiod(self, host_name, service_description, notification_timeperiod):
        """
        Changes the notification timeperiod for a particular service to what is
        specified by the "notification_timeperiod" option.  The
        "notification_timeperiod" option should be the short name of the timeperiod that
        is to be used as the service notification timeperiod.  The timeperiod must have
        been configured in Nagios before it was last (re)started.
        """
        self.run('CHANGE_SVC_NOTIFICATION_TIMEPERIOD', host_name, service_description, notification_timeperiod)

    def delay_host_notification(self, host_name, notification_time):
        """
        Delays the next notification for a parciular service until "notification_time".
        The "notification_time" argument is specified in time_t format (seconds since
        the UNIX epoch).  Note that this will only have an affect if the service stays
        in the same problem state that it is currently in.  If the service changes to
        another state, a new notification may go out before the time you specify in the
        "notification_time" argument.
        """
        self.run('DELAY_HOST_NOTIFICATION', host_name, notification_time)

    def delay_svc_notification(self, host_name, service_description, notification_time):
        """
        Delays the next notification for a parciular service until "notification_time".
        The "notification_time" argument is specified in time_t format (seconds since
        the UNIX epoch).  Note that this will only have an affect if the service stays
        in the same problem state that it is currently in.  If the service changes to
        another state, a new notification may go out before the time you specify in the
        "notification_time" argument.
        """
        self.run('DELAY_SVC_NOTIFICATION', host_name, service_description, notification_time)

    def del_all_host_comments(self, host_name):
        """
        Deletes all comments assocated with a particular host.
        """
        self.run('DEL_ALL_HOST_COMMENTS', host_name)

    def del_all_svc_comments(self, host_name, service_description):
        """
        Deletes all comments associated with a particular service.
        """
        self.run('DEL_ALL_SVC_COMMENTS', host_name, service_description)

    def del_host_comment(self, comment_id):
        """
        Deletes a host comment.  The id number of the comment that is to be deleted must
        be specified.
        """
        self.run('DEL_HOST_COMMENT', comment_id)

    def del_host_downtime(self, downtime_id):
        """
        Deletes the host downtime entry that has an ID number matching the "downtime_id"
        argument.  If the downtime is currently in effect, the host will come out of
        scheduled downtime (as long as there are no other overlapping active downtime
        entries).
        """
        self.run('DEL_HOST_DOWNTIME', downtime_id)

    def del_svc_comment(self, comment_id):
        """
        Deletes a service comment.  The id number of the comment that is to be deleted
        must be specified.
        """
        self.run('DEL_SVC_COMMENT', comment_id)

    def del_svc_downtime(self, downtime_id):
        """
        Deletes the service downtime entry that has an ID number matching the
        "downtime_id" argument.  If the downtime is currently in effect, the service
        will come out of scheduled downtime (as long as there are no other overlapping
        active downtime entries).
        """
        self.run('DEL_SVC_DOWNTIME', downtime_id)

    def disable_all_notifications_beyond_host(self, host_name):
        """
        Disables notifications for all hosts and services "beyond" (e.g. on all child
        hosts of) the specified host.  The current notification setting for the
        specified host is not affected.
        """
        self.run('DISABLE_ALL_NOTIFICATIONS_BEYOND_HOST', host_name)

    def disable_contactgroup_host_notifications(self, contactgroup_name):
        """
        Disables host notifications for all contacts in a particular contactgroup.
        """
        self.run('DISABLE_CONTACTGROUP_HOST_NOTIFICATIONS', contactgroup_name)

    def disable_contactgroup_svc_notifications(self, contactgroup_name):
        """
        Disables service notifications for all contacts in a particular contactgroup.
        """
        self.run('DISABLE_CONTACTGROUP_SVC_NOTIFICATIONS', contactgroup_name)

    def disable_contact_host_notifications(self, contact_name):
        """
        Disables host notifications for a particular contact.
        """
        self.run('DISABLE_CONTACT_HOST_NOTIFICATIONS', contact_name)

    def disable_contact_svc_notifications(self, contact_name):
        """
        Disables service notifications for a particular contact.
        """
        self.run('DISABLE_CONTACT_SVC_NOTIFICATIONS', contact_name)

    def disable_event_handlers(self, ):
        """
        Disables host and service event handlers on a program-wide basis.
        """
        self.run('DISABLE_EVENT_HANDLERS', )

    def disable_failure_prediction(self, ):
        """
        Disables failure prediction on a program-wide basis.  This feature is not
        currently implemented in Nagios.
        """
        self.run('DISABLE_FAILURE_PREDICTION', )

    def disable_flap_detection(self, ):
        """
        Disables host and service flap detection on a program-wide basis.
        """
        self.run('DISABLE_FLAP_DETECTION', )

    def disable_hostgroup_host_checks(self, hostgroup_name):
        """
        Disables active checks for all hosts in a particular hostgroup.
        """
        self.run('DISABLE_HOSTGROUP_HOST_CHECKS', hostgroup_name)

    def disable_hostgroup_host_notifications(self, hostgroup_name):
        """
        Disables notifications for all hosts in a particular hostgroup.  This does not
        disable notifications for the services associated with the hosts in the
        hostgroup - see the DISABLE_HOSTGROUP_SVC_NOTIFICATIONS command for that.
        """
        self.run('DISABLE_HOSTGROUP_HOST_NOTIFICATIONS', hostgroup_name)

    def disable_hostgroup_passive_host_checks(self, hostgroup_name):
        """
        Disables passive checks for all hosts in a particular hostgroup.
        """
        self.run('DISABLE_HOSTGROUP_PASSIVE_HOST_CHECKS', hostgroup_name)

    def disable_hostgroup_passive_svc_checks(self, hostgroup_name):
        """
        Disables passive checks for all services associated with hosts in a particular
        hostgroup.
        """
        self.run('DISABLE_HOSTGROUP_PASSIVE_SVC_CHECKS', hostgroup_name)

    def disable_hostgroup_svc_checks(self, hostgroup_name):
        """
        Disables active checks for all services associated with hosts in a particular
        hostgroup.
        """
        self.run('DISABLE_HOSTGROUP_SVC_CHECKS', hostgroup_name)

    def disable_hostgroup_svc_notifications(self, hostgroup_name):
        """
        Disables notifications for all services associated with hosts in a particular
        hostgroup.  This does not disable notifications for the hosts in the hostgroup -
        see the DISABLE_HOSTGROUP_HOST_NOTIFICATIONS command for that.
        """
        self.run('DISABLE_HOSTGROUP_SVC_NOTIFICATIONS', hostgroup_name)

    def disable_host_and_child_notifications(self, host_name):
        """
        Disables notifications for the specified host, as well as all hosts "beyond"
        (e.g. on all child hosts of) the specified host.
        """
        self.run('DISABLE_HOST_AND_CHILD_NOTIFICATIONS', host_name)

    def disable_host_check(self, host_name):
        """
        Disables (regularly scheduled and on-demand) active checks of the specified
        host.
        """
        self.run('DISABLE_HOST_CHECK', host_name)

    def disable_host_event_handler(self, host_name):
        """
        Disables the event handler for the specified host.
        """
        self.run('DISABLE_HOST_EVENT_HANDLER', host_name)

    def disable_host_flap_detection(self, host_name):
        """
        Disables flap detection for the specified host.
        """
        self.run('DISABLE_HOST_FLAP_DETECTION', host_name)

    def disable_host_freshness_checks(self, ):
        """
        Disables freshness checks of all hosts on a program-wide basis.
        """
        self.run('DISABLE_HOST_FRESHNESS_CHECKS', )

    def disable_host_notifications(self, host_name):
        """
        Disables notifications for a particular host.
        """
        self.run('DISABLE_HOST_NOTIFICATIONS', host_name)

    def disable_host_svc_checks(self, host_name):
        """
        Enables active checks of all services on the specified host.
        """
        self.run('DISABLE_HOST_SVC_CHECKS', host_name)

    def disable_host_svc_notifications(self, host_name):
        """
        Disables notifications for all services on the specified host.
        """
        self.run('DISABLE_HOST_SVC_NOTIFICATIONS', host_name)

    def disable_notifications(self, ):
        """
        Disables host and service notifications on a program-wide basis.
        """
        self.run('DISABLE_NOTIFICATIONS', )

    def disable_passive_host_checks(self, host_name):
        """
        Disables acceptance and processing of passive host checks for the specified
        host.
        """
        self.run('DISABLE_PASSIVE_HOST_CHECKS', host_name)

    def disable_passive_svc_checks(self, host_name, service_description):
        """
        Disables passive checks for the specified service.
        """
        self.run('DISABLE_PASSIVE_SVC_CHECKS', host_name, service_description)

    def disable_performance_data(self, ):
        """
        Disables the processing of host and service performance data on a program-wide
        basis.
        """
        self.run('DISABLE_PERFORMANCE_DATA', )

    def disable_servicegroup_host_checks(self, servicegroup_name):
        """
        Disables active checks for all hosts that have services that are members of a
        particular hostgroup.
        """
        self.run('DISABLE_SERVICEGROUP_HOST_CHECKS', servicegroup_name)

    def disable_servicegroup_host_notifications(self, servicegroup_name):
        """
        Disables notifications for all hosts that have services that are members of a
        particular servicegroup.
        """
        self.run('DISABLE_SERVICEGROUP_HOST_NOTIFICATIONS', servicegroup_name)

    def disable_servicegroup_passive_host_checks(self, servicegroup_name):
        """
        Disables the acceptance and processing of passive checks for all hosts that have
        services that are members of a particular service group.
        """
        self.run('DISABLE_SERVICEGROUP_PASSIVE_HOST_CHECKS', servicegroup_name)

    def disable_servicegroup_passive_svc_checks(self, servicegroup_name):
        """
        Disables the acceptance and processing of passive checks for all services in a
        particular servicegroup.
        """
        self.run('DISABLE_SERVICEGROUP_PASSIVE_SVC_CHECKS', servicegroup_name)

    def disable_servicegroup_svc_checks(self, servicegroup_name):
        """
        Disables active checks for all services in a particular servicegroup.
        """
        self.run('DISABLE_SERVICEGROUP_SVC_CHECKS', servicegroup_name)

    def disable_servicegroup_svc_notifications(self, servicegroup_name):
        """
        Disables notifications for all services that are members of a particular
        servicegroup.
        """
        self.run('DISABLE_SERVICEGROUP_SVC_NOTIFICATIONS', servicegroup_name)

    def disable_service_flap_detection(self, host_name, service_description):
        """
        Disables flap detection for the specified service.
        """
        self.run('DISABLE_SERVICE_FLAP_DETECTION', host_name, service_description)

    def disable_service_freshness_checks(self, ):
        """
        Disables freshness checks of all services on a program-wide basis.
        """
        self.run('DISABLE_SERVICE_FRESHNESS_CHECKS', )

    def disable_svc_check(self, host_name, service_description):
        """
        Disables active checks for a particular service.
        """
        self.run('DISABLE_SVC_CHECK', host_name, service_description)

    def disable_svc_event_handler(self, host_name, service_description):
        """
        Disables the event handler for the specified service.
        """
        self.run('DISABLE_SVC_EVENT_HANDLER', host_name, service_description)

    def disable_svc_flap_detection(self, host_name, service_description):
        """
        Disables flap detection for the specified service.
        """
        self.run('DISABLE_SVC_FLAP_DETECTION', host_name, service_description)

    def disable_svc_notifications(self, host_name, service_description):
        """
        Disables notifications for a particular service.
        """
        self.run('DISABLE_SVC_NOTIFICATIONS', host_name, service_description)

    def enable_all_notifications_beyond_host(self, host_name):
        """
        Enables notifications for all hosts and services "beyond" (e.g. on all child
        hosts of) the specified host.  The current notification setting for the
        specified host is not affected.  Notifications will only be sent out for these
        hosts and services if notifications are also enabled on a program-wide basis.
        """
        self.run('ENABLE_ALL_NOTIFICATIONS_BEYOND_HOST', host_name)

    def enable_contactgroup_host_notifications(self, contactgroup_name):
        """
        Enables host notifications for all contacts in a particular contactgroup.
        """
        self.run('ENABLE_CONTACTGROUP_HOST_NOTIFICATIONS', contactgroup_name)

    def enable_contactgroup_svc_notifications(self, contactgroup_name):
        """
        Enables service notifications for all contacts in a particular contactgroup.
        """
        self.run('ENABLE_CONTACTGROUP_SVC_NOTIFICATIONS', contactgroup_name)

    def enable_contact_host_notifications(self, contact_name):
        """
        Enables host notifications for a particular contact.
        """
        self.run('ENABLE_CONTACT_HOST_NOTIFICATIONS', contact_name)

    def enable_contact_svc_notifications(self, contact_name):
        """
        Disables service notifications for a particular contact.
        """
        self.run('ENABLE_CONTACT_SVC_NOTIFICATIONS', contact_name)

    def enable_event_handlers(self, ):
        """
        Enables host and service event handlers on a program-wide basis.
        """
        self.run('ENABLE_EVENT_HANDLERS', )

    def enable_failure_prediction(self, ):
        """
        Enables failure prediction on a program-wide basis.  This feature is not
        currently implemented in Nagios.
        """
        self.run('ENABLE_FAILURE_PREDICTION', )

    def enable_flap_detection(self, ):
        """
        Enables host and service flap detection on a program-wide basis.
        """
        self.run('ENABLE_FLAP_DETECTION', )

    def enable_hostgroup_host_checks(self, hostgroup_name):
        """
        Enables active checks for all hosts in a particular hostgroup.
        """
        self.run('ENABLE_HOSTGROUP_HOST_CHECKS', hostgroup_name)

    def enable_hostgroup_host_notifications(self, hostgroup_name):
        """
        Enables notifications for all hosts in a particular hostgroup.  This does not
        enable notifications for the services associated with the hosts in the hostgroup
        - see the ENABLE_HOSTGROUP_SVC_NOTIFICATIONS command for that.  In order for
        notifications to be sent out for these hosts, notifications must be enabled on a
        program-wide basis as well.
        """
        self.run('ENABLE_HOSTGROUP_HOST_NOTIFICATIONS', hostgroup_name)

    def enable_hostgroup_passive_host_checks(self, hostgroup_name):
        """
        Enables passive checks for all hosts in a particular hostgroup.
        """
        self.run('ENABLE_HOSTGROUP_PASSIVE_HOST_CHECKS', hostgroup_name)

    def enable_hostgroup_passive_svc_checks(self, hostgroup_name):
        """
        Enables passive checks for all services associated with hosts in a particular
        hostgroup.
        """
        self.run('ENABLE_HOSTGROUP_PASSIVE_SVC_CHECKS', hostgroup_name)

    def enable_hostgroup_svc_checks(self, hostgroup_name):
        """
        Enables active checks for all services associated with hosts in a particular
        hostgroup.
        """
        self.run('ENABLE_HOSTGROUP_SVC_CHECKS', hostgroup_name)

    def enable_hostgroup_svc_notifications(self, hostgroup_name):
        """
        Enables notifications for all services that are associated with hosts in a
        particular hostgroup.  This does not enable notifications for the hosts in the
        hostgroup - see the ENABLE_HOSTGROUP_HOST_NOTIFICATIONS command for that.  In
        order for notifications to be sent out for these services, notifications must be
        enabled on a program-wide basis as well.
        """
        self.run('ENABLE_HOSTGROUP_SVC_NOTIFICATIONS', hostgroup_name)

    def enable_host_and_child_notifications(self, host_name):
        """
        Enables notifications for the specified host, as well as all hosts "beyond"
        (e.g. on all child hosts of) the specified host.  Notifications will only be
        sent out for these hosts if notifications are also enabled on a program-wide
        basis.
        """
        self.run('ENABLE_HOST_AND_CHILD_NOTIFICATIONS', host_name)

    def enable_host_check(self, host_name):
        """
        Enables (regularly scheduled and on-demand) active checks of the specified
        host.
        """
        self.run('ENABLE_HOST_CHECK', host_name)

    def enable_host_event_handler(self, host_name):
        """
        Enables the event handler for the specified host.
        """
        self.run('ENABLE_HOST_EVENT_HANDLER', host_name)

    def enable_host_flap_detection(self, host_name):
        """
        Enables flap detection for the specified host.  In order for the flap detection
        algorithms to be run for the host, flap detection must be enabled on a
        program-wide basis as well.
        """
        self.run('ENABLE_HOST_FLAP_DETECTION', host_name)

    def enable_host_freshness_checks(self, ):
        """
        Enables freshness checks of all hosts on a program-wide basis.  Individual hosts
        that have freshness checks disabled will not be checked for freshness.
        """
        self.run('ENABLE_HOST_FRESHNESS_CHECKS', )

    def enable_host_notifications(self, host_name):
        """
        Enables notifications for a particular host.  Notifications will be sent out for
        the host only if notifications are enabled on a program-wide basis as well.
        """
        self.run('ENABLE_HOST_NOTIFICATIONS', host_name)

    def enable_host_svc_checks(self, host_name):
        """
        Enables active checks of all services on the specified host.
        """
        self.run('ENABLE_HOST_SVC_CHECKS', host_name)

    def enable_host_svc_notifications(self, host_name):
        """
        Enables notifications for all services on the specified host.  Note that
        notifications will not be sent out if notifications are disabled on a
        program-wide basis.
        """
        self.run('ENABLE_HOST_SVC_NOTIFICATIONS', host_name)

    def enable_notifications(self, ):
        """
        Enables host and service notifications on a program-wide basis.
        """
        self.run('ENABLE_NOTIFICATIONS', )

    def enable_passive_host_checks(self, host_name):
        """
        Enables acceptance and processing of passive host checks for the specified
        host.
        """
        self.run('ENABLE_PASSIVE_HOST_CHECKS', host_name)

    def enable_passive_svc_checks(self, host_name, service_description):
        """
        Enables passive checks for the specified service.
        """
        self.run('ENABLE_PASSIVE_SVC_CHECKS', host_name, service_description)

    def enable_performance_data(self, ):
        """
        Enables the processing of host and service performance data on a program-wide
        basis.
        """
        self.run('ENABLE_PERFORMANCE_DATA', )

    def enable_servicegroup_host_checks(self, servicegroup_name):
        """
        Enables active checks for all hosts that have services that are members of a
        particular hostgroup.
        """
        self.run('ENABLE_SERVICEGROUP_HOST_CHECKS', servicegroup_name)

    def enable_servicegroup_host_notifications(self, servicegroup_name):
        """
        Enables notifications for all hosts that have services that are members of a
        particular servicegroup.  In order for notifications to be sent out for these
        hosts, notifications must also be enabled on a program-wide basis.
        """
        self.run('ENABLE_SERVICEGROUP_HOST_NOTIFICATIONS', servicegroup_name)

    def enable_servicegroup_passive_host_checks(self, servicegroup_name):
        """
        Enables the acceptance and processing of passive checks for all hosts that have
        services that are members of a particular service group.
        """
        self.run('ENABLE_SERVICEGROUP_PASSIVE_HOST_CHECKS', servicegroup_name)

    def enable_servicegroup_passive_svc_checks(self, servicegroup_name):
        """
        Enables the acceptance and processing of passive checks for all services in a
        particular servicegroup.
        """
        self.run('ENABLE_SERVICEGROUP_PASSIVE_SVC_CHECKS', servicegroup_name)

    def enable_servicegroup_svc_checks(self, servicegroup_name):
        """
        Enables active checks for all services in a particular servicegroup.
        """
        self.run('ENABLE_SERVICEGROUP_SVC_CHECKS', servicegroup_name)

    def enable_servicegroup_svc_notifications(self, servicegroup_name):
        """
        Enables notifications for all services that are members of a particular
        servicegroup.  In order for notifications to be sent out for these services,
        notifications must also be enabled on a program-wide basis.
        """
        self.run('ENABLE_SERVICEGROUP_SVC_NOTIFICATIONS', servicegroup_name)

    def enable_service_freshness_checks(self, ):
        """
        Enables freshness checks of all services on a program-wide basis.  Individual
        services that have freshness checks disabled will not be checked for freshness.
        """
        self.run('ENABLE_SERVICE_FRESHNESS_CHECKS', )

    def enable_svc_check(self, host_name, service_description):
        """
        Enables active checks for a particular service.
        """
        self.run('ENABLE_SVC_CHECK', host_name, service_description)

    def enable_svc_event_handler(self, host_name, service_description):
        """
        Enables the event handler for the specified service.
        """
        self.run('ENABLE_SVC_EVENT_HANDLER', host_name, service_description)

    def enable_svc_flap_detection(self, host_name, service_description):
        """
        Enables flap detection for the specified service.  In order for the flap
        detection algorithms to be run for the service, flap detection must be enabled
        on a program-wide basis as well.
        """
        self.run('ENABLE_SVC_FLAP_DETECTION', host_name, service_description)

    def enable_svc_notifications(self, host_name, service_description):
        """
        Enables notifications for a particular service.  Notifications will be sent out
        for the service only if notifications are enabled on a program-wide basis as
        well.
        """
        self.run('ENABLE_SVC_NOTIFICATIONS', host_name, service_description)

    def process_file(self, file_name, delete):
        """
        Directs Nagios to process all external commands that are found in the file
        specified by the <file_name> argument.  If the <delete> option is non-zero, the
        file will be deleted once it has been processes.  If the <delete> option is set
        to zero, the file is left untouched.
        """
        self.run('PROCESS_FILE', file_name, delete)

    def process_host_check_result(self, host_name, status_code, plugin_output):
        """
        This is used to submit a passive check result for a particular host.  The
        "status_code" indicates the state of the host check and should be one of the
        following: 0=UP, 1=DOWN, 2=UNREACHABLE.  The "plugin_output" argument contains
        the text returned from the host check, along with optional performance data.
        """
        self.run('PROCESS_HOST_CHECK_RESULT', host_name, status_code, plugin_output)

    def process_service_check_result(self, host_name, service_description, return_code, plugin_output):
        """
        This is used to submit a passive check result for a particular service.  The
        "return_code" field should be one of the following: 0=OK, 1=WARNING, 2=CRITICAL,
        3=UNKNOWN.  The "plugin_output" field contains text output from the service
        check, along with optional performance data.
        """
        self.run('PROCESS_SERVICE_CHECK_RESULT', host_name, service_description, return_code, plugin_output)

    def read_state_information(self, ):
        """
        Causes Nagios to load all current monitoring status information from the state
        retention file.  Normally, state retention information is loaded when the Nagios
        process starts up and before it starts monitoring.  WARNING: This command will
        cause Nagios to discard all current monitoring status information and use the
        information stored in state retention file!  Use with care.
        """
        self.run('READ_STATE_INFORMATION', )

    def remove_host_acknowledgement(self, host_name):
        """
        This removes the problem acknowledgement for a particular host.  Once the
        acknowledgement has been removed, notifications can once again be sent out for
        the given host.
        """
        self.run('REMOVE_HOST_ACKNOWLEDGEMENT', host_name)

    def remove_svc_acknowledgement(self, host_name, service_description):
        """
        This removes the problem acknowledgement for a particular service.  Once the
        acknowledgement has been removed, notifications can once again be sent out for
        the given service.
        """
        self.run('REMOVE_SVC_ACKNOWLEDGEMENT', host_name, service_description)

    def restart_program(self, ):
        """
        Restarts the Nagios process.
        """
        self.run('RESTART_PROGRAM', )

    def save_state_information(self, ):
        """
        Causes Nagios to save all current monitoring status information to the state
        retention file.  Normally, state retention information is saved before the
        Nagios process shuts down and (potentially) at regularly scheduled intervals.
        This command allows you to force Nagios to save this information to the state
        retention file immediately.  This does not affect the current status information
        in the Nagios process.
        """
        self.run('SAVE_STATE_INFORMATION', )

    def schedule_and_propagate_host_downtime(self, host_name, start_time, end_time, fixed, trigger_id, duration, author, comment):
        """
        Schedules downtime for a specified host and all of its children (hosts).  If the
        "fixed" argument is set to one (1), downtime will start and end at the times
        specified by the "start" and "end" arguments.  Otherwise, downtime will begin
        between the "start" and "end" times and last for "duration" seconds.  The
        "start" and "end" arguments are specified in time_t format (seconds since the
        UNIX epoch).  The specified (parent) host downtime can be triggered by another
        downtime entry if the "trigger_id" is set to the ID of another scheduled
        downtime entry.  Set the "trigger_id" argument to zero (0) if the downtime for
        the specified (parent) host should not be triggered by another downtime entry.
        """
        self.run('SCHEDULE_AND_PROPAGATE_HOST_DOWNTIME', host_name, start_time, end_time, fixed, trigger_id, duration, author, comment)

    def schedule_and_propagate_triggered_host_downtime(self, host_name, start_time, end_time, fixed, trigger_id, duration, author, comment):
        """
        Schedules downtime for a specified host and all of its children (hosts).  If the
        "fixed" argument is set to one (1), downtime will start and end at the times
        specified by the "start" and "end" arguments.  Otherwise, downtime will begin
        between the "start" and "end" times and last for "duration" seconds.  The
        "start" and "end" arguments are specified in time_t format (seconds since the
        UNIX epoch).  Downtime for child hosts are all set to be triggered by the
        downtime for the specified (parent) host.  The specified (parent) host downtime
        can be triggered by another downtime entry if the "trigger_id" is set to the ID
        of another scheduled downtime entry.  Set the "trigger_id" argument to zero (0)
        if the downtime for the specified (parent) host should not be triggered by
        another downtime entry.
        """
        self.run('SCHEDULE_AND_PROPAGATE_TRIGGERED_HOST_DOWNTIME', host_name, start_time, end_time, fixed, trigger_id, duration, author, comment)

    def schedule_forced_host_check(self, host_name, check_time):
        """
        Schedules a forced active check of a particular host at "check_time".  The
        "check_time" argument is specified in time_t format (seconds since the UNIX
        epoch).   Forced checks are performed regardless of what time it is (e.g.
        timeperiod restrictions are ignored) and whether or not active checks are
        enabled on a host-specific or program-wide basis.
        """
        self.run('SCHEDULE_FORCED_HOST_CHECK', host_name, check_time)

    def schedule_forced_host_svc_checks(self, host_name, check_time):
        """
        Schedules a forced active check of all services associated with a particular
        host at "check_time".  The "check_time" argument is specified in time_t format
        (seconds since the UNIX epoch).   Forced checks are performed regardless of what
        time it is (e.g. timeperiod restrictions are ignored) and whether or not active
        checks are enabled on a service-specific or program-wide basis.
        """
        self.run('SCHEDULE_FORCED_HOST_SVC_CHECKS', host_name, check_time)

    def schedule_forced_svc_check(self, host_name, service_description, check_time):
        """
        Schedules a forced active check of a particular service at "check_time".  The
        "check_time" argument is specified in time_t format (seconds since the UNIX
        epoch).   Forced checks are performed regardless of what time it is (e.g.
        timeperiod restrictions are ignored) and whether or not active checks are
        enabled on a service-specific or program-wide basis.
        """
        self.run('SCHEDULE_FORCED_SVC_CHECK', host_name, service_description, check_time)

    def schedule_hostgroup_host_downtime(self, hostgroup_name, start_time, end_time, fixed, trigger_id, duration, author, comment):
        """
        Schedules downtime for all hosts in a specified hostgroup.  If the "fixed"
        argument is set to one (1), downtime will start and end at the times specified
        by the "start" and "end" arguments.  Otherwise, downtime will begin between the
        "start" and "end" times and last for "duration" seconds.  The "start" and "end"
        arguments are specified in time_t format (seconds since the UNIX epoch).  The
        host downtime entries can be triggered by another downtime entry if the
        "trigger_id" is set to the ID of another scheduled downtime entry.  Set the
        "trigger_id" argument to zero (0) if the downtime for the hosts should not be
        triggered by another downtime entry.
        """
        self.run('SCHEDULE_HOSTGROUP_HOST_DOWNTIME', hostgroup_name, start_time, end_time, fixed, trigger_id, duration, author, comment)

    def schedule_hostgroup_svc_downtime(self, hostgroup_name, start_time, end_time, fixed, trigger_id, duration, author, comment):
        """
        Schedules downtime for all services associated with hosts in a specified
        servicegroup.  If the "fixed" argument is set to one (1), downtime will start
        and end at the times specified by the "start" and "end" arguments.  Otherwise,
        downtime will begin between the "start" and "end" times and last for "duration"
        seconds.  The "start" and "end" arguments are specified in time_t format
        (seconds since the UNIX epoch).  The service downtime entries can be triggered
        by another downtime entry if the "trigger_id" is set to the ID of another
        scheduled downtime entry.  Set the "trigger_id" argument to zero (0) if the
        downtime for the services should not be triggered by another downtime entry.
        """
        self.run('SCHEDULE_HOSTGROUP_SVC_DOWNTIME', hostgroup_name, start_time, end_time, fixed, trigger_id, duration, author, comment)

    def schedule_host_check(self, host_name, check_time):
        """
        Schedules the next active check of a particular host at "check_time".  The
        "check_time" argument is specified in time_t format (seconds since the UNIX
        epoch).  Note that the host may not actually be checked at the time you specify.
        This could occur for a number of reasons: active checks are disabled on a
        program-wide or service-specific basis, the host is already scheduled to be
        checked at an earlier time, etc.  If you want to force the host check to occur
        at the time you specify, look at the SCHEDULE_FORCED_HOST_CHECK command.
        """
        self.run('SCHEDULE_HOST_CHECK', host_name, check_time)

    def schedule_host_downtime(self, host_name, start_time, end_time, fixed, trigger_id, duration, author, comment):
        """
        Schedules downtime for a specified host.  If the "fixed" argument is set to one
        (1), downtime will start and end at the times specified by the "start" and "end"
        arguments.  Otherwise, downtime will begin between the "start" and "end" times
        and last for "duration" seconds.  The "start" and "end" arguments are specified
        in time_t format (seconds since the UNIX epoch).  The specified host downtime
        can be triggered by another downtime entry if the "trigger_id" is set to the ID
        of another scheduled downtime entry.  Set the "trigger_id" argument to zero (0)
        if the downtime for the specified host should not be triggered by another
        downtime entry.
        """
        self.run('SCHEDULE_HOST_DOWNTIME', host_name, start_time, end_time, fixed, trigger_id, duration, author, comment)

    def schedule_host_svc_checks(self, host_name, check_time):
        """
        Schedules the next active check of all services on a particular host at
        "check_time".  The "check_time" argument is specified in time_t format (seconds
        since the UNIX epoch).  Note that the services may not actually be checked at
        the time you specify.  This could occur for a number of reasons: active checks
        are disabled on a program-wide or service-specific basis, the services are
        already scheduled to be checked at an earlier time, etc.  If you want to force
        the service checks to occur at the time you specify, look at the
        SCHEDULE_FORCED_HOST_SVC_CHECKS command.
        """
        self.run('SCHEDULE_HOST_SVC_CHECKS', host_name, check_time)

    def schedule_host_svc_downtime(self, host_name, start_time, end_time, fixed, trigger_id, duration, author, comment):
        """
        Schedules downtime for all services associated with a particular host.  If the
        "fixed" argument is set to one (1), downtime will start and end at the times
        specified by the "start" and "end" arguments.  Otherwise, downtime will begin
        between the "start" and "end" times and last for "duration" seconds.  The
        "start" and "end" arguments are specified in time_t format (seconds since the
        UNIX epoch).  The service downtime entries can be triggered by another downtime
        entry if the "trigger_id" is set to the ID of another scheduled downtime entry.
        Set the "trigger_id" argument to zero (0) if the downtime for the services
        should not be triggered by another downtime entry.
        """
        self.run('SCHEDULE_HOST_SVC_DOWNTIME', host_name, start_time, end_time, fixed, trigger_id, duration, author, comment)

    def schedule_servicegroup_host_downtime(self, servicegroup_name, start_time, end_time, fixed, trigger_id, duration, author, comment):
        """
        Schedules downtime for all hosts that have services in a specified servicegroup.
        If the "fixed" argument is set to one (1), downtime will start and end at the
        times specified by the "start" and "end" arguments.  Otherwise, downtime will
        begin between the "start" and "end" times and last for "duration" seconds.  The
        "start" and "end" arguments are specified in time_t format (seconds since the
        UNIX epoch).  The host downtime entries can be triggered by another downtime
        entry if the "trigger_id" is set to the ID of another scheduled downtime entry.
        Set the "trigger_id" argument to zero (0) if the downtime for the hosts should
        not be triggered by another downtime entry.
        """
        self.run('SCHEDULE_SERVICEGROUP_HOST_DOWNTIME', servicegroup_name, start_time, end_time, fixed, trigger_id, duration, author, comment)

    def schedule_servicegroup_svc_downtime(self, servicegroup_name, start_time, end_time, fixed, trigger_id, duration, author, comment):
        """
        Schedules downtime for all services in a specified servicegroup.  If the "fixed"
        argument is set to one (1), downtime will start and end at the times specified
        by the "start" and "end" arguments.  Otherwise, downtime will begin between the
        "start" and "end" times and last for "duration" seconds.  The "start" and "end"
        arguments are specified in time_t format (seconds since the UNIX epoch).  The
        service downtime entries can be triggered by another downtime entry if the
        "trigger_id" is set to the ID of another scheduled downtime entry.  Set the
        "trigger_id" argument to zero (0) if the downtime for the services should not be
        triggered by another downtime entry.
        """
        self.run('SCHEDULE_SERVICEGROUP_SVC_DOWNTIME', servicegroup_name, start_time, end_time, fixed, trigger_id, duration, author, comment)

    def schedule_svc_check(self, host_name, service_description, check_time):
        """
        Schedules the next active check of a specified service at "check_time".  The
        "check_time" argument is specified in time_t format (seconds since the UNIX
        epoch).  Note that the service may not actually be checked at the time you
        specify.  This could occur for a number of reasons: active checks are disabled
        on a program-wide or service-specific basis, the service is already scheduled to
        be checked at an earlier time, etc.  If you want to force the service check to
        occur at the time you specify, look at the SCHEDULE_FORCED_SVC_CHECK command.
        """
        self.run('SCHEDULE_SVC_CHECK', host_name, service_description, check_time)

    def schedule_svc_downtime(self, host_name, service_desriptionstart_time, end_time, fixed, trigger_id, duration, author, comment):
        """
        Schedules downtime for a specified service.  If the "fixed" argument is set to
        one (1), downtime will start and end at the times specified by the "start" and
        "end" arguments.  Otherwise, downtime will begin between the "start" and "end"
        times and last for "duration" seconds.  The "start" and "end" arguments are
        specified in time_t format (seconds since the UNIX epoch).  The specified
        service downtime can be triggered by another downtime entry if the "trigger_id"
        is set to the ID of another scheduled downtime entry.  Set the "trigger_id"
        argument to zero (0) if the downtime for the specified service should not be
        triggered by another downtime entry.
        """
        self.run('SCHEDULE_SVC_DOWNTIME', host_name, service_desriptionstart_time, end_time, fixed, trigger_id, duration, author, comment)

    def send_custom_host_notification(self, host_name, options, author, comment):
        """
        Allows you to send a custom host notification.  Very useful in dire situations,
        emergencies or to communicate with all admins that are responsible for a
        particular host.  When the host notification is sent out, the $NOTIFICATIONTYPE$
        macro will be set to "CUSTOM".  The <options> field is a logical OR of the
        following integer values that affect aspects of the notification that are sent
        out: 0 = No option (default), 1 = Broadcast (send notification to all normal and
        all escalated contacts for the host), 2 = Forced (notification is sent out
        regardless of current time, whether or not notifications are enabled, etc.), 4 =
        Increment current notification # for the host (this is not done by default for
        custom notifications).  The comment field can be used with the
        $NOTIFICATIONCOMMENT$ macro in notification commands.
        """
        self.run('SEND_CUSTOM_HOST_NOTIFICATION', host_name, options, author, comment)

    def send_custom_svc_notification(self, host_name, service_description, options, author, comment):
        """
        Allows you to send a custom service notification.  Very useful in dire
        situations, emergencies or to communicate with all admins that are responsible
        for a particular service.  When the service notification is sent out, the
        $NOTIFICATIONTYPE$ macro will be set to "CUSTOM".  The <options> field is a
        logical OR of the following integer values that affect aspects of the
        notification that are sent out: 0 = No option (default), 1 = Broadcast (send
        notification to all normal and all escalated contacts for the service), 2 =
        Forced (notification is sent out regardless of current time, whether or not
        notifications are enabled, etc.), 4 = Increment current notification # for the
        service(this is not done by default for custom notifications).   The comment
        field can be used with the $NOTIFICATIONCOMMENT$ macro in notification
        commands.
        """
        self.run('SEND_CUSTOM_SVC_NOTIFICATION', host_name, service_description, options, author, comment)

    def set_host_notification_number(self, host_name, notification_number):
        """
        Sets the current notification number for a particular host.  A value of 0
        indicates that no notification has yet been sent for the current host problem.
        Useful for forcing an escalation (based on notification number) or replicating
        notification information in redundant monitoring environments. Notification
        numbers greater than zero have no noticeable affect on the notification process
        if the host is currently in an UP state.
        """
        self.run('SET_HOST_NOTIFICATION_NUMBER', host_name, notification_number)

    def set_svc_notification_number(self, host_name, service_description, notification_number):
        """
        Sets the current notification number for a particular service.  A value of 0
        indicates that no notification has yet been sent for the current service
        problem.  Useful for forcing an escalation (based on notification number) or
        replicating notification information in redundant monitoring environments.
        Notification numbers greater than zero have no noticeable affect on the
        notification process if the service is currently in an OK state.
        """
        self.run('SET_SVC_NOTIFICATION_NUMBER', host_name, service_description, notification_number)

    def shutdown_program(self, ):
        """
        Shuts down the Nagios process.
        """
        self.run('SHUTDOWN_PROGRAM', )

    def start_accepting_passive_host_checks(self, ):
        """
        Enables acceptance and processing of passive host checks on a program-wide
        basis.
        """
        self.run('START_ACCEPTING_PASSIVE_HOST_CHECKS', )

    def start_accepting_passive_svc_checks(self, ):
        """
        Enables passive service checks on a program-wide basis.
        """
        self.run('START_ACCEPTING_PASSIVE_SVC_CHECKS', )

    def start_executing_host_checks(self, ):
        """
        Enables active host checks on a program-wide basis.
        """
        self.run('START_EXECUTING_HOST_CHECKS', )

    def start_executing_svc_checks(self, ):
        """
        Enables active checks of services on a program-wide basis.
        """
        self.run('START_EXECUTING_SVC_CHECKS', )

    def start_obsessing_over_host(self, host_name):
        """
        Enables processing of host checks via the OCHP command for the specified host.
        """
        self.run('START_OBSESSING_OVER_HOST', host_name)

    def start_obsessing_over_host_checks(self, ):
        """
        Enables processing of host checks via the OCHP command on a program-wide basis.
        """
        self.run('START_OBSESSING_OVER_HOST_CHECKS', )

    def start_obsessing_over_svc(self, host_name, service_description):
        """
        Enables processing of service checks via the OCSP command for the specified
        service.
        """
        self.run('START_OBSESSING_OVER_SVC', host_name, service_description)

    def start_obsessing_over_svc_checks(self, ):
        """
        Enables processing of service checks via the OCSP command on a program-wide
        basis.
        """
        self.run('START_OBSESSING_OVER_SVC_CHECKS', )

    def stop_accepting_passive_host_checks(self, ):
        """
        Disables acceptance and processing of passive host checks on a program-wide
        basis.
        """
        self.run('STOP_ACCEPTING_PASSIVE_HOST_CHECKS', )

    def stop_accepting_passive_svc_checks(self, ):
        """
        Disables passive service checks on a program-wide basis.
        """
        self.run('STOP_ACCEPTING_PASSIVE_SVC_CHECKS', )

    def stop_executing_host_checks(self, ):
        """
        Disables active host checks on a program-wide basis.
        """
        self.run('STOP_EXECUTING_HOST_CHECKS', )

    def stop_executing_svc_checks(self, ):
        """
        Disables active checks of services on a program-wide basis.
        """
        self.run('STOP_EXECUTING_SVC_CHECKS', )

    def stop_obsessing_over_host(self, host_name):
        """
        Disables processing of host checks via the OCHP command for the specified host.
        """
        self.run('STOP_OBSESSING_OVER_HOST', host_name)

    def stop_obsessing_over_host_checks(self, ):
        """
        Disables processing of host checks via the OCHP command on a program-wide
        basis.
        """
        self.run('STOP_OBSESSING_OVER_HOST_CHECKS', )

    def stop_obsessing_over_svc(self, host_name, service_description):
        """
        Disables processing of service checks via the OCSP command for the specified
        service.
        """
        self.run('STOP_OBSESSING_OVER_SVC', host_name, service_description)

    def stop_obsessing_over_svc_checks(self, ):
        """
        Disables processing of service checks via the OCSP command on a program-wide
        basis.
        """
        self.run('STOP_OBSESSING_OVER_SVC_CHECKS', )

