VALID_CATEGORIES = ["Network", "Hardware", "Software", "Other"]
VALID_URGENCIES = ["low", "medium", "high"]


def calculate_priority(urgency, affected_users):
    if urgency == "high" and affected_users >= 10:
        return "critical"
    if urgency == "high" or affected_users >= 10:
        return "high"
    if urgency == "medium" or affected_users >= 3:
        return "medium"
    return "low"


def validate_title(title):
    if not isinstance(title, str) or title.strip() == "":
        raise ValueError("Title must not be blank.")
    return title.strip()


def validate_category(category):
    if not isinstance(category, str):
        raise ValueError("Category must be text.")
    cleaned = category.strip().capitalize()
    if cleaned not in VALID_CATEGORIES:
        raise ValueError(
            f"Category must be one of: {', '.join(VALID_CATEGORIES)}."
        )
    return cleaned


def validate_urgency(urgency):
    if not isinstance(urgency, str):
        raise ValueError("Urgency must be text.")
    cleaned = urgency.strip().lower()
    if cleaned not in VALID_URGENCIES:
        raise ValueError(
            f"Urgency must be one of: {', '.join(VALID_URGENCIES)}."
        )
    return cleaned


def validate_affected_users(affected_users):
    if isinstance(affected_users, bool) or not isinstance(affected_users, int):
        raise ValueError("Affected users must be a whole number.")
    if affected_users <= 0:
        raise ValueError("Affected users must be greater than zero.")
    return affected_users


def generate_ticket_id(tickets):
    highest = 0
    for ticket in tickets:
        number = int(ticket["id"][1:])
        if number > highest:
            highest = number
    return f"T{highest + 1:03d}"


def create_ticket(tickets, title, category, urgency, affected_users):
    title = validate_title(title)
    category = validate_category(category)
    urgency = validate_urgency(urgency)
    affected_users = validate_affected_users(affected_users)

    ticket = {
        "id": generate_ticket_id(tickets),
        "title": title,
        "category": category,
        "urgency": urgency,
        "affected_users": affected_users,
        "priority": calculate_priority(urgency, affected_users),
        "status": "open",
        "assigned_to": None,
    }
    tickets.append(ticket)
    return ticket