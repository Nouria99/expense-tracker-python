#Expense Tracker System Python Testing Code
#created by: Nouria Bellamri
#Date: 20/09/2024

import os
import unittest
from unittest.mock import patch
from Task2 import load_data, save_data, login, register, add_expense, update_expense, delete_expense, set_budget, generate_report

class TestTask2(unittest.TestCase):
    USER_FILE = "user_test.json"

    def setUp(self):
        self.test_data = {
            "Nouria95": {
                "password": "prog456",
                "expenses": [],
                "budget": None
            }
        }
        save_data(self.test_data, self.USER_FILE)

    def tearDown(self):
        if os.path.exists(self.USER_FILE):
            os.remove(self.USER_FILE)

    def test_register(self):
        # Register a new user
        register(file_name=self.USER_FILE)
        data = load_data(file_name=self.USER_FILE)
        self.assertIn("new_user", data)
        self.assertEqual(data["new_user"]["password"], "new_pass") 

    @patch('builtins.input', side_effect=["Nouria95", "prog456"])
    def test_login_success(self, mock_input):
        # Test successful login
        Username = login(file_name=self.USER_FILE)
        self.assertEqual(Username, "Nouria95")

    @patch('builtins.input', side_effect=["Nouria95", "wrong_pass"])
    def test_login_failure(self, mock_input):
        # Test failed login
        Username = login(file_name=self.USER_FILE)
        self.assertIsNone(Username)

    @patch('builtins.input', side_effect=["Lunch", "15.0", "Food"])
    def test_add_expense(self, mock_input):
        #Add an expense and test its addition
        add_expense("Nouria95", "Lunch", 15.0, "Food", file_name=self.USER_FILE)
        data = load_data(file_name=self.USER_FILE)
        self.assertEqual(len(data["Nouria95"]["expenses"]), 1)
        self.assertEqual(data["Nouria95"]["expenses"][0]["description"], "Lunch")
    
    @patch('builtins.input', side_effect=["Dinner", "20.0", "Food"])
    def test_update_expense(self, mock_input):
        #Update an expense and test its update
        add_expense("Nouria95", "Lunch", 15.0, "Food", file_name=self.USER_FILE)
        update_expense("Nouria95", expense_id=0, description="Dinner", amount=20.0, category="Food", file_name=self.USER_FILE)
        data = load_data(file_name=self.USER_FILE)
        self.assertEqual(data["Nouria95"]["expenses"][0]["description"], "Dinner")
    
    @patch('builtins.input', side_effect=[1])
    def test_delete_expense(self, mock_input):
        #Delete an expense and test its deletion
        add_expense("Nouria95", "Lunch", 15.0, "Food", file_name=self.USER_FILE)
        delete_expense("Nouria95", expense_id=0, file_name=self.USER_FILE)
        data = load_data(file_name=self.USER_FILE)
        self.assertEqual(len(data["Nouria95"]["expenses"]), 0)
    
    @patch('builtins.input', side_effect=[650.0])
    def test_set_budget(self, mock_input):
        # Set a budget and test its setting
        set_budget("Nouria95", budget=650.0, file_name=self.USER_FILE)
        data = load_data(file_name=self.USER_FILE)
        self.assertEqual(data["Nouria95"]["budget"], 650.0)

    def test_generate_report(self):
        #Generate and test the expense report
        add_expense("Nouria95", "Lunch", 15.0, "Food", file_name=self.USER_FILE)
        report = generate_report("Nouria95", file_name=self.USER_FILE)
        self.assertIn("Expenses report for Nouria95", report)
        self.assertIn("Total spent:", report)

if __name__ == "__main__":
    unittest.main()



    
