import unittest
from campusflow.tickets import (
    calculate_priority,
    validate_title,
    validate_category,
    validate_urgency,
    validate_affected_users,
    generate_ticket_id,
    create_ticket,
)


class TestPriority(unittest.TestCase):
    def test_high_urgency_many_users_is_critical(self):
        self.assertEqual(calculate_priority("high", 12), "critical")

    def test_high_urgency_few_users_is_high(self):
        self.assertEqual(calculate_priority("high", 2), "high")

    def test_low_urgency_some_users_is_medium(self):
        self.assertEqual(calculate_priority("low", 4), "medium")

    def test_low_urgency_one_user_is_low(self):
        self.assertEqual(calculate_priority("low", 1), "low")


class TestValidateTitle(unittest.TestCase):
    def test_blank_title_rejected(self):
        with self.assertRaises(ValueError):
            validate_title("   ")

    def test_valid_title_is_stripped(self):
        self.assertEqual(validate_title("  Wi-Fi down  "), "Wi-Fi down")


class TestValidateCategory(unittest.TestCase):
    def test_category_case_is_normalized(self):
        self.assertEqual(validate_category("  nEtWoRk "), "Network")

    def test_unknown_category_rejected(self):
        with self.assertRaises(ValueError):
            validate_category("Plumbing")


class TestValidateUrgency(unittest.TestCase):
    def test_urgency_case_is_normalized(self):
        self.assertEqual(validate_urgency("HIGH"), "high")

    def test_unknown_urgency_rejected(self):
        with self.assertRaises(ValueError):
            validate_urgency("urgent")


class TestValidateAffectedUsers(unittest.TestCase):
    def test_zero_rejected(self):
        with self.assertRaises(ValueError):
            validate_affected_users(0)

    def test_negative_rejected(self):
        with self.assertRaises(ValueError):
            validate_affected_users(-3)

    def test_decimal_rejected(self):
        with self.assertRaises(ValueError):
            validate_affected_users(2.5)

    def test_text_rejected(self):
        with self.assertRaises(ValueError):
            validate_affected_users("abc")

    def test_valid_number_accepted(self):
        self.assertEqual(validate_affected_users(15), 15)


class TestGenerateTicketId(unittest.TestCase):
    def test_first_id_is_t001(self):
        self.assertEqual(generate_ticket_id([]), "T001")

    def test_next_id_follows_highest(self):
        existing = [{"id": "T001"}, {"id": "T002"}]
        self.assertEqual(generate_ticket_id(existing), "T003")

    def test_gap_in_ids_does_not_duplicate(self):
        existing = [{"id": "T001"}, {"id": "T005"}]
        self.assertEqual(generate_ticket_id(existing), "T006")


class TestCreateTicket(unittest.TestCase):
    def test_create_ticket_success(self):
        tickets = []
        ticket = create_ticket(tickets, "Wi-Fi down", "network", "HIGH", 15)
        self.assertEqual(ticket["id"], "T001")
        self.assertEqual(ticket["category"], "Network")
        self.assertEqual(ticket["priority"], "critical")
        self.assertEqual(ticket["status"], "open")
        self.assertIsNone(ticket["assigned_to"])
        self.assertEqual(len(tickets), 1)

    def test_invalid_ticket_not_stored(self):
        tickets = []
        with self.assertRaises(ValueError):
            create_ticket(tickets, "Wi-Fi down", "Network", "high", 0)
        self.assertEqual(tickets, [])

    def test_second_ticket_gets_next_id(self):
        tickets = []
        create_ticket(tickets, "Wi-Fi down", "Network", "high", 15)
        second = create_ticket(tickets, "Laptop broken", "Hardware", "low", 1)
        self.assertEqual(second["id"], "T002")


if __name__ == "__main__":
    unittest.main()
