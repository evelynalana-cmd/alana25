from app.data.tickets import (
    insert_ticket, get_all_tickets, get_tickets_by_status,
    get_tickets_by_priority, get_tickets_by_assigned,
    update_ticket, delete_ticket
)

def create_ticket(**kwargs):
    return insert_ticket(**kwargs)

def list_tickets():
    return get_all_tickets()

def list_tickets_by_status(status):
    return get_tickets_by_status(status)

def list_tickets_by_priority(priority):
    return get_tickets_by_priority(priority)

def list_tickets_by_assigned(assigned_to):
    return get_tickets_by_assigned(assigned_to)

def modify_ticket(ticket_id, **kwargs):
    update_ticket(ticket_id, **kwargs)

def remove_ticket(ticket_id):
    delete_ticket(ticket_id)