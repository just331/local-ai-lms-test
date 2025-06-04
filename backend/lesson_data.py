lesson_rubrics = {
    "logic_programming": {
        "answer_set_programming_definition": {
            "definition": (
                "Answer Set Programming (ASP) is a declarative programming paradigm "
                "oriented towards difficult search problems; it is based on logic programming and nonmonotonic "
                "reasoning."
                "In ASP, solutions are represented as 'answer sets' for a given logic program."
            ),
            "rubric": [
                "Mentions ASP is a declarative programming paradigm",
                "Mentions logic programming/nonmonotonic reasoning",
                "Mentions answer sets/solutions",
            ],
            "expected_keywords": [
                "declarative", "logic programming", "nonmonotonic", "answer sets", "search problems"
            ]
        },
        "asp_ancestor_definition": {
            "definition": (
                "ancestor(X,Y) :- parent(X,Y).\n"
                "ancestor(X,Y) :- parent(X,Z), ancestor(Z,Y)."
            ),
            "rubric": [
                "Defines the base case: ancestor(X,Y) :- parent(X,Y).",
                "Defines the recursive case: ancestor(X,Y) :- parent(X,Z), ancestor(Z,Y).",
                "Uses correct ASP syntax.",
                "Variables are capitalized and used consistently.",
            ],
            "expected_keywords": [
                "parent", "ancestor", ":-", ","
            ]
        }
    },
    "numbers_functions_expressions": {
        "function_comprehension": {
            "definition": (
            ),
            "rubric": [
            ],
            "expected_keywords": [
            ]
        },
        "expression_comprehension": {
            "definition": (
            ),
            "rubric": [
            ],
            "expected_keywords": [
            ]
        },

    },
    "statistics": {
        "s1": {
            "definition": (
            ),
            "rubric": [
            ],
            "expected_keywords": [
            ]
        },
        "s2": {
            "definition": (
            ),
            "rubric": [
            ],
            "expected_keywords": [
            ]
        },
    },
}
