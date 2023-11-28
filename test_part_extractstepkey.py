from model import Part

class TestExtractStepkey:

    #  Should return the entire key and None if there are no parentheses in the input string.
    def test_no_parentheses(self):
        part = Part()
        result = part.extract_stepkey("key")
        assert result == ("key", None)

    #  Should return the key and the step number as a tuple if the input string contains parentheses.
    def test_with_parentheses(self):
        part = Part()
        result = part.extract_stepkey("key(1)")
        assert result == ("key", "1")

    #  Should correctly split the input string into key and step number, removing the parentheses and any whitespace.
    def test_split_string(self):
        part = Part()
        result = part.extract_stepkey(" key ( 1 ) ")
        assert result == ("key", "1")

    #  Should return an empty string and None if the input string is an empty string.
    def test_empty_string(self):
        part = Part()
        result = part.extract_stepkey("")
        assert result == ("", None)

    #  Should return the entire input string and None if the input string only contains parentheses.
    def test_only_parentheses(self):
        part = Part()
        result = part.extract_stepkey("()")
        assert result == ("", "")

    #  Should return the entire input string and None if the input string contains only one parenthesis.
    def test_one_parenthesis(self):
        part = Part()
        result = part.extract_stepkey("(")
        assert result == ("(", None)

    #  Should return the key and an empty string if the input string contains parentheses but no step number.
    def test_no_step_number(self):
        part = Part()
        result = part.extract_stepkey("key()")
        assert result == ("key", "")

    #  Should return the key and empty string if the input string contains parentheses but no step number,
    #  and the parentheses are not at the end of the string.
    def test_no_step_number_not_at_end(self):
        part = Part()
        result = part.extract_stepkey("key()text")
        assert result == ("key", "")

    #  Should handle input strings with multiple sets of parentheses correctly.
    def test_multiple_parentheses(self):
        part = Part()
        result = part.extract_stepkey("key(1)(2)")
        assert result == ("key", "1")

    #  Handling nested parentheses is not required
    def test_nested_parentheses(self):
        part = Part()
        result = part.extract_stepkey("key(1(2))")
        assert result == ("key", "1(2")

    #  Should handle input strings with non-numeric step numbers correctly.
    def test_non_numeric_step_number(self):
        part = Part()
        result = part.extract_stepkey("key(a)")
        assert result == ("key", "a")

    #  Should handle input strings with negative step numbers correctly.
    def test_negative_step_number(self):
        part = Part()
        result = part.extract_stepkey("key(-1)")
        assert result == ("key", "-1")
