# This file is kept as placeholder for potential database models
# Currently, we're not using a database for this application
# but this file can be expanded when adding user authentication, 
# saving analysis results, etc.

class DentalCondition:
    def __init__(self, id, name, symptoms, solutions, severity_level):
        self.id = id
        self.name = name
        self.symptoms = symptoms
        self.solutions = solutions
        self.severity_level = severity_level  # 1-5 scale
