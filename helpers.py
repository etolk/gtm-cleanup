from ratelimit import limits, sleep_and_retry

# Rate limit settings
CALLS = 15
PERIOD = 60



def delete_unused_triggers(source_workspace):
    while delete_triggers(source_workspace) > 0:
        pass


def delete_triggers(source_workspace):
    deleted = 0
    for trigger in source_workspace.triggers:
        if delete_trigger(trigger):
            deleted += 1
    return deleted

@sleep_and_retry
@limits(calls=CALLS, period=PERIOD)
def delete_trigger(trigger):
    # print("Delete delete_trigger", gtm_key, trigger.name)
    depended = trigger.get_depended()
    if depended["len"] == 0:
        # print("Realy Delete delete_trigger", gtm_key, trigger.name)
        print(f"Delete trigger: {trigger.name}")
        trigger.delete()
        # time.sleep(10)
        return True
        

def delete_unused_variables(source_workspace):
    while delete_variables(source_workspace) > 0:
        pass


def delete_variables(source_workspace):
    deleted = 0
    for variable in source_workspace.variables:
        if delete_variable(variable):
                deleted += 1
    return deleted

@sleep_and_retry
@limits(calls=CALLS, period=PERIOD)
def delete_variable(variable):
    depended = variable.get_depended()
    if depended["len"] == 0:
        print(f"Delete variable: {variable.name}")
        variable.delete()
        # time.sleep(10)
        return True