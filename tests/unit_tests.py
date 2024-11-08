import unittest
from unittest.mock import patch, mock_open
from src.dependency_resolver import parse_file, find_all_dependencies

class TestDependencyParser(unittest.TestCase):
    """Unit tests for parse_file function"""
    
    @patch('os.path.isfile')  # Mock file existence check
    def test_parse_single_dependency(self, mock_isfile):
        """Test parsing single dependency line"""
        mock_isfile.return_value = True  # Simulate file exists
        mock_content = "A depends on B"
        with patch('builtins.open', mock_open(read_data=mock_content)):
            with patch('os.path.getsize', return_value=len(mock_content)):  # Mock file size
                deps, order = parse_file("dummy.txt")
                self.assertEqual(deps, {'A': ['B']})
                self.assertEqual(order, ['A'])
    
    @patch('os.path.isfile')
    def test_parse_multiple_dependencies(self, mock_isfile):
        """Test parsing multiple dependencies on single line"""
        mock_isfile.return_value = True
        mock_content = "A depends on B C D"
        with patch('builtins.open', mock_open(read_data=mock_content)):
            with patch('os.path.getsize', return_value=len(mock_content)):
                deps, order = parse_file("dummy.txt")
                self.assertEqual(deps, {'A': ['B', 'C', 'D']})
                self.assertEqual(order, ['A'])
    
    @patch('os.path.isfile')
    def test_parse_multiple_lines(self, mock_isfile):
        """Test parsing multiple lines"""
        mock_isfile.return_value = True
        mock_content = "A depends on B C\nB depends on D\nC depends on E"
        with patch('builtins.open', mock_open(read_data=mock_content)):
            with patch('os.path.getsize', return_value=len(mock_content)):
                deps, order = parse_file("dummy.txt")
                self.assertEqual(deps, {
                    'A': ['B', 'C'],
                    'B': ['D'],
                    'C': ['E']
                })
                self.assertEqual(order, ['A', 'B', 'C'])
    
    @patch('os.path.isfile')
    def test_empty_file(self, mock_isfile):
        """Test parsing empty file"""
        mock_isfile.return_value = True
        mock_content = ""
        with patch('builtins.open', mock_open(read_data=mock_content)):
            with patch('os.path.getsize', return_value=0):
                deps, order = parse_file("dummy.txt")
                self.assertEqual(deps, {})
                self.assertEqual(order, [])
    
    @patch('os.path.isfile')
    def test_whitespace_variations(self, mock_isfile):
        """Test parsing with various whitespace patterns"""
        mock_isfile.return_value = True
        mock_content = "A   depends    on    B    C"
        with patch('builtins.open', mock_open(read_data=mock_content)):
            with patch('os.path.getsize', return_value=len(mock_content)):
                deps, order = parse_file("dummy.txt")
                self.assertEqual(deps, {'A': ['B', 'C']})
                self.assertEqual(order, ['A'])
    
    @patch('os.path.isfile')
    def test_invalid_syntax(self, mock_isfile):
        """Test invalid syntax raises ValueError"""
        mock_isfile.return_value = True
        mock_content = "A depends B C"
        with patch('builtins.open', mock_open(read_data=mock_content)):
            with patch('os.path.getsize', return_value=len(mock_content)):
                with self.assertRaises(ValueError):
                    parse_file("dummy.txt")
    
    @patch('os.path.isfile')
    def test_invalid_chars(self, mock_isfile):
        """Test invalid characters raise ValueError"""
        mock_isfile.return_value = True
        mock_content = "A@ depends on B"
        with patch('builtins.open', mock_open(read_data=mock_content)):
            with patch('os.path.getsize', return_value=len(mock_content)):
                with self.assertRaises(ValueError):
                    parse_file("dummy.txt")
    
    @patch('os.path.isfile')
    def test_self_dependency(self, mock_isfile):
        """Test self dependency raises ValueError"""
        mock_isfile.return_value = True
        mock_content = "A depends on A"
        with patch('builtins.open', mock_open(read_data=mock_content)):
            with patch('os.path.getsize', return_value=len(mock_content)):
                with self.assertRaises(ValueError):
                    parse_file("dummy.txt")
    
    def test_file_not_found(self):
        """Test handling of non-existent file"""
        with patch('os.path.isfile', return_value=False):
            with self.assertRaises(FileNotFoundError):
                parse_file("nonexistent.txt")

    @patch('os.path.isfile')
    def test_duplicate_library_declaration(self, mock_isfile):
        """Test when same library is declared multiple times"""
        mock_isfile.return_value = True
        mock_content = "A depends on B\nA depends on C"
        with patch('builtins.open', mock_open(read_data=mock_content)):
            with patch('os.path.getsize', return_value=len(mock_content)):
                deps, order = parse_file("dummy.txt")
                # Should keep last declaration
                self.assertEqual(deps, {'A': ['C']})
                # Should maintain first appearance in order
                self.assertEqual(order, ['A'])
    
    @patch('os.path.isfile')
    def test_empty_dependencies(self, mock_isfile):
        """Test library with no dependencies"""
        mock_isfile.return_value = True
        mock_content = "A depends on"
        with patch('builtins.open', mock_open(read_data=mock_content)):
            with patch('os.path.getsize', return_value=len(mock_content)):
                deps, order = parse_file("dummy.txt")
                self.assertEqual(deps, {'A': []})




class TestDependencyResolver(unittest.TestCase):
    """Unit tests for find_all_dependencies function"""
    
    def test_single_level_dependency(self):
        """Test finding dependencies with one level"""
        deps = {'A': ['B', 'C']}
        result = find_all_dependencies('A', deps)
        self.assertEqual(result, {'B', 'C'})
    
    def test_transitive_dependency(self):
        """Test finding transitive dependencies"""
        deps = {
            'A': ['B'],
            'B': ['C']
        }
        result = find_all_dependencies('A', deps)
        self.assertEqual(result, {'B', 'C'})
    
    def test_circular_dependency(self):
        """Test handling circular dependencies"""
        deps = {
            'A': ['B'],
            'B': ['C'],
            'C': ['A']
        }
        result = find_all_dependencies('A', deps)
        self.assertEqual(result, {'B', 'C'})
    
    def test_missing_dependency(self):
        """Test handling missing dependencies"""
        deps = {
            'A': ['B', 'C'],
            'B': ['D']  # D is not defined
        }
        result = find_all_dependencies('A', deps)
        self.assertEqual(result, {'B', 'C', 'D'})
    
    def test_complex_dependencies(self):
        """Test complex dependency chain"""
        deps = {
            'A': ['B', 'C'],
            'B': ['D', 'E'],
            'C': ['F'],
            'D': ['G'],
            'E': ['H'],
            'F': ['I']
        }
        result = find_all_dependencies('A', deps)
        self.assertEqual(result, {'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'})

    def test_no_dependencies_found(self):
        """Test when library has no dependencies"""
        deps = {'A': []}
        result = find_all_dependencies('A', deps)
        self.assertEqual(result, set())
    

if __name__ == '__main__':
    unittest.main()