from datetime import datetime, timezone


def delete_unused_triggers(source_workspace):
    while delete_triggers(source_workspace) > 0:
        pass


def delete_triggers(source_workspace):
    deleted = 0
    for trigger in source_workspace.triggers:
        if delete_trigger(trigger):
            deleted += 1
    return deleted


def delete_trigger(trigger):
    depended = trigger.get_depended()
    if depended["len"] == 0:
        print(f"Delete trigger: {trigger.name}")
        trigger.delete()
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


def delete_variable(variable):
    depended = variable.get_depended()
    if depended["len"] == 0:
        print(f"Delete variable: {variable.name}")
        variable.delete()
        return True
    
def delete_paused_tags(source_workspace):
    print("Deleting paused tags")
    for tag in [tag for tag in source_workspace.tags if tag.isPaused()]:
        tag.delete()
        print(f"Deleted tag: {tag.name}")

def delete_expired_tags(source_workspace):
    print("Deleting expired tags")
    for tag in [tag for tag in source_workspace.tags]:
        if 'scheduleEndMs' in tag.data:
            schedule_end_ms = int(tag.data['scheduleEndMs'])
            schedule_end_date = datetime.fromtimestamp(schedule_end_ms / 1000.0, tz=timezone.utc)
            current_date = datetime.now(tz=timezone.utc)
            if schedule_end_date < current_date:
                tag.delete()
                print(f"Deleted tag: {tag.name}")