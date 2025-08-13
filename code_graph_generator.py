#!/usr/bin/env python3
"""
Code Graph Generator for ScarySingleDocs Repository
This script performs static analysis of the codebase and generates a machine-readable code graph.
"""

import os
import ast
import json
import pathlib
import nbformat
import argparse
from typing import Dict, List, Set, Optional, Any


class CodeGraphGenerator:
    def __init__(self, repo_root: str):
        self.repo_root = pathlib.Path(repo_root)
        self.nodes = {}  # node_id -> node_data
        self.edges = []  # list of edge_data
        self.node_counter = 0
        self.visited_files = set()
        
        # Track function and class definitions across all files
        self.function_definitions = {}  # name -> node_id
        self.class_definitions = {}     # name -> node_id
        
    def get_next_node_id(self) -> str:
        """Generate a unique node ID."""
        self.node_counter += 1
        return f"node_{self.node_counter}"
    
    def add_node(self, node_id: str, node_type: str, name: str, file_path: str = "", 
                 line_number: int = 0, **kwargs) -> str:
        """Add a node to the graph."""
        self.nodes[node_id] = {
            "id": node_id,
            "type": node_type,
            "name": name,
            "file_path": file_path,
            "line_number": line_number,
            **kwargs
        }
        return node_id
    
    def add_edge(self, source_id: str, target_id: str, edge_type: str, **kwargs):
        """Add an edge to the graph."""
        edge_data = {
            "source": source_id,
            "target": target_id,
            "type": edge_type,
            **kwargs
        }
        self.edges.append(edge_data)
    
    def parse_notebook(self, notebook_path: str) -> List[str]:
        """Parse a Jupyter notebook and extract executed scripts."""
        executed_scripts = []
        
        try:
            with open(notebook_path, 'r', encoding='utf-8') as f:
                notebook = nbformat.read(f, as_version=4)
            
            notebook_node_id = self.get_next_node_id()
            self.add_node(notebook_node_id, "File", str(notebook_path), str(notebook_path))
            
            # Extract variable definitions from the first cell
            variables = {
                'lang': 'en',
                'branch': 'main',
                'scripts_dir': '/home/z/my-project/ScarySingleDocs/scripts'
            }
            
            for cell_idx, cell in enumerate(notebook.cells):
                if cell.cell_type == "code":
                    source = ''.join(cell.source) if isinstance(cell.source, list) else cell.source
                    
                    # Look for %run or !exec commands
                    lines = source.split('\n')
                    for line_num, line in enumerate(lines):
                        line = line.strip()
                        if line.startswith('%run') or line.startswith('!'):
                            # Extract script path
                            script_path = line.split(maxsplit=1)[1] if len(line.split()) > 1 else ""
                            script_path = script_path.strip()
                            
                            # Handle variable substitution
                            resolved_path = script_path
                            for var_name, var_value in variables.items():
                                resolved_path = resolved_path.replace(f'${var_name}', var_value)
                            
                            # Handle f-string like formatting
                            resolved_path = resolved_path.replace('{branch}', variables.get('branch', 'main'))
                            resolved_path = resolved_path.replace('{lang}', variables.get('lang', 'en'))
                            
                            # Try to resolve the actual file path
                            actual_path = self.resolve_script_path(resolved_path, str(pathlib.Path(notebook_path).parent))
                            
                            if actual_path:
                                executed_scripts.append(actual_path)
                                script_node_id = self.get_next_node_id()
                                self.add_node(script_node_id, "Script", resolved_path, 
                                            str(notebook_path), line_num + 1, actual_path=actual_path)
                                self.add_edge(notebook_node_id, script_node_id, "EXECUTES")
                            else:
                                # Add as unresolved script
                                script_node_id = self.get_next_node_id()
                                self.add_node(script_node_id, "UnresolvedScript", resolved_path, 
                                            str(notebook_path), line_num + 1)
                                self.add_edge(notebook_node_id, script_node_id, "EXECUTES")
        
        except Exception as e:
            print(f"Error parsing notebook {notebook_path}: {e}")
        
        return executed_scripts
    
    def parse_python_file(self, file_path: str) -> Dict[str, Any]:
        """Parse a Python file and extract its structure."""
        result = {
            'imports': [],
            'functions': [],
            'classes': [],
            'calls': []
        }
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            
            # Add file node
            file_node_id = self.get_next_node_id()
            self.add_node(file_node_id, "File", str(file_path), str(file_path))
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        result['imports'].append(alias.name)
                        import_node_id = self.get_next_node_id()
                        self.add_node(import_node_id, "Module", alias.name, str(file_path), 
                                    node.lineno)
                        self.add_edge(file_node_id, import_node_id, "IMPORTS")
                
                elif isinstance(node, ast.ImportFrom):
                    module_name = node.module or ""
                    for alias in node.names:
                        full_name = f"{module_name}.{alias.name}" if module_name else alias.name
                        result['imports'].append(full_name)
                        import_node_id = self.get_next_node_id()
                        self.add_node(import_node_id, "Module", full_name, str(file_path), 
                                    node.lineno)
                        self.add_edge(file_node_id, import_node_id, "IMPORTS")
                        
                        # Special handling for _season import in setup.py
                        if "setup.py" in file_path and module_name == "_season":
                            # Also try to find the module file directly
                            _season_path = self._find_import_file("_season", str(pathlib.Path(file_path).parent))
                            if _season_path:
                                if _season_path not in self.visited_files:
                                    # Add this to the results for processing
                                    result['imports'].append("_season")
                                    import_node_id = self.get_next_node_id()
                                    self.add_node(import_node_id, "Module", "_season", str(file_path), 
                                                node.lineno)
                                    self.add_edge(file_node_id, import_node_id, "IMPORTS")
                
                elif isinstance(node, ast.FunctionDef):
                    func_name = f"{file_path}::{node.name}"
                    result['functions'].append(func_name)
                    func_node_id = self.get_next_node_id()
                    self.add_node(func_node_id, "Function", node.name, str(file_path), 
                                node.lineno)
                    self.add_edge(file_node_id, func_node_id, "DEFINES")
                    
                    # Track function definition for call resolution
                    self.function_definitions[node.name] = func_node_id
                    
                    # Parse function body for calls, instantiations, and file I/O
                    self._parse_function_body_enhanced(node, func_node_id, file_path)
                
                elif isinstance(node, ast.ClassDef):
                    class_name = f"{file_path}::{node.name}"
                    result['classes'].append(class_name)
                    class_node_id = self.get_next_node_id()
                    self.add_node(class_node_id, "Class", node.name, str(file_path), 
                                node.lineno)
                    self.add_edge(file_node_id, class_node_id, "DEFINES")
                    
                    # Track class definition for instantiation resolution
                    self.class_definitions[node.name] = class_node_id
                    
                    # Parse class methods
                    for item in node.body:
                        if isinstance(item, ast.FunctionDef):
                            method_name = f"{file_path}::{node.name}.{item.name}"
                            result['functions'].append(method_name)
                            method_node_id = self.get_next_node_id()
                            self.add_node(method_node_id, "Method", item.name, str(file_path), 
                                        item.lineno, class_name=node.name)
                            self.add_edge(class_node_id, method_node_id, "DEFINES")
                            
                            # Track method definition for call resolution
                            full_method_name = f"{node.name}.{item.name}"
                            self.function_definitions[full_method_name] = method_node_id
                            
                            # Parse method body
                            self._parse_function_body_enhanced(item, method_node_id, file_path)
        
        except Exception as e:
            print(f"Error parsing Python file {file_path}: {e}")
        
        return result
    
    def _parse_function_body_enhanced(self, func_node: ast.FunctionDef, func_node_id: str, file_path: str):
        """Enhanced function body parser to extract calls, instantiations, and file I/O."""
        for node in ast.walk(func_node):
            if isinstance(node, ast.Call):
                # Extract function name and create call node
                func_name = self._extract_call_name(node)
                if func_name:
                    call_node_id = self.get_next_node_id()
                    self.add_node(call_node_id, "Call", func_name, str(file_path), 
                                node.lineno)
                    self.add_edge(func_node_id, call_node_id, "CALLS")
                    
                    # Check if this is a class instantiation
                    if self._is_class_instantiation(node):
                        class_name = func_name.split('(')[0]  # Remove constructor arguments
                        if class_name in self.class_definitions:
                            self.add_edge(func_node_id, self.class_definitions[class_name], "INSTANTIATES")
                    
                    # Check for file I/O operations
                    self._analyze_file_io(node, func_node_id, file_path)
            
            # Look for file operations in assignments
            elif isinstance(node, ast.Assign):
                self._analyze_assignment_for_file_io(node, func_node_id, file_path)
    
    def _is_class_instantiation(self, call_node: ast.Call) -> bool:
        """Check if a call node represents a class instantiation."""
        # Simple heuristic: if the call is to a name that could be a class
        if isinstance(call_node.func, ast.Name):
            return True  # Could be a class instantiation
        elif isinstance(call_node.func, ast.Attribute):
            return True  # Could be a class method or attribute
        return False
    
    def _analyze_file_io(self, call_node: ast.Call, func_node_id: str, file_path: str):
        """Analyze call nodes for file I/O operations."""
        func_name = self._extract_call_name(call_node)
        
        # Check for built-in file operations
        if func_name in ['open', 'json.load', 'json.loads', 'json.dump', 'json.dumps']:
            # Look for file path arguments
            if call_node.args:
                for arg in call_node.args[:1]:  # Usually first argument is file path
                    if isinstance(arg, (ast.Str, ast.Constant)):
                        file_path_str = arg.s if isinstance(arg, ast.Str) else arg.value
                        if isinstance(file_path_str, str):
                            self._add_file_io_node(func_node_id, file_path_str, file_path, 
                                                  "READS_FROM" if 'load' in func_name else "WRITES_TO")
                    elif isinstance(arg, ast.Name):
                        # Variable reference - we can't resolve the actual file path statically
                        pass
    
    def _analyze_assignment_for_file_io(self, assign_node: ast.Assign, func_node_id: str, file_path: str):
        """Analyze assignment nodes for file I/O operations."""
        # Look for patterns like: f = open(...) or data = json.load(...)
        if isinstance(assign_node.value, ast.Call):
            call_node = assign_node.value
            func_name = self._extract_call_name(call_node)
            
            if func_name in ['open', 'json.load', 'json.loads', 'json.dump', 'json.dumps']:
                # Look for file path arguments
                if call_node.args:
                    for arg in call_node.args[:1]:  # Usually first argument is file path
                        if isinstance(arg, (ast.Str, ast.Constant)):
                            file_path_str = arg.s if isinstance(arg, ast.Str) else arg.value
                            if isinstance(file_path_str, str):
                                self._add_file_io_node(func_node_id, file_path_str, file_path, 
                                                      "READS_FROM" if 'load' in func_name else "WRITES_TO")
    
    def _add_file_io_node(self, func_node_id: str, file_path_str: str, source_file_path: str, io_type: str):
        """Add a file node and I/O edge to the graph."""
        # Create a unique file node ID
        file_node_id = f"file_{file_path_str.replace('/', '_').replace('.', '_')}"
        
        # Add file node if it doesn't exist
        if file_node_id not in self.nodes:
            self.add_node(file_node_id, "File", file_path_str, file_path_str)
        
        # Add I/O edge
        self.add_edge(func_node_id, file_node_id, io_type)
    
    def _parse_function_body(self, func_node: ast.FunctionDef, func_node_id: str, file_path: str):
        """Legacy function body parser (deprecated)."""
        # This method is kept for backward compatibility but should not be used
        self._parse_function_body_enhanced(func_node, func_node_id, file_path)
    
    def _extract_call_name(self, call_node: ast.Call) -> Optional[str]:
        """Extract the function name from a call node."""
        if isinstance(call_node.func, ast.Name):
            return call_node.func.id
        elif isinstance(call_node.func, ast.Attribute):
            return self._get_attribute_chain(call_node.func)
        elif isinstance(call_node.func, ast.Subscript):
            return self._get_subscript_name(call_node.func)
        return None
    
    def _get_attribute_chain(self, node: ast.Attribute) -> str:
        """Get the full attribute chain (e.g., obj.method.submethod)."""
        if isinstance(node.value, ast.Name):
            return f"{node.value.id}.{node.attr}"
        elif isinstance(node.value, ast.Attribute):
            return f"{self._get_attribute_chain(node.value)}.{node.attr}"
        return node.attr
    
    def _get_subscript_name(self, node: ast.Subscript) -> str:
        """Get the name from a subscript node."""
        if isinstance(node.value, ast.Name):
            return f"{node.value.id}[...]"
        elif isinstance(node.value, ast.Attribute):
            return f"{self._get_attribute_chain(node.value)}[...]"
        return "[...]"
    
    def resolve_script_path(self, script_path: str, current_dir: str) -> Optional[str]:
        """Resolve a script path to an actual file path."""
        # Handle relative paths
        if script_path.startswith('./'):
            script_path = script_path[2:]
        
        # Handle URLs (skip these)
        if script_path.startswith('http://') or script_path.startswith('https://'):
            return None
        
        # Handle curl commands (skip these)
        if 'curl' in script_path:
            return None
        
        # Clean up the path
        script_path = script_path.strip()
        
        # Try to resolve the path
        possible_paths = [
            pathlib.Path(current_dir) / script_path,
            self.repo_root / script_path,
            self.repo_root / "scripts" / script_path,
            self.repo_root / "scripts" / "en" / script_path,
            pathlib.Path.home() / "ScarySingleDocs" / "scripts" / script_path,
        ]
        
        # Also try with .py extension
        if not script_path.endswith('.py'):
            possible_paths.extend([
                pathlib.Path(current_dir) / f"{script_path}.py",
                self.repo_root / f"{script_path}.py",
                self.repo_root / "scripts" / f"{script_path}.py",
                self.repo_root / "scripts" / "en" / f"{script_path}.py",
                pathlib.Path.home() / "ScarySingleDocs" / "scripts" / f"{script_path}.py",
            ])
        
        for path in possible_paths:
            if path.exists() and path.suffix in ['.py']:
                return str(path)
        
        return None
    
    def analyze_repository(self, entry_point: str):
        """Analyze the repository starting from the entry point.
        
        Args:
            entry_point: Path to the entry point (can be a notebook or Python script)
        """
        print(f"Start Analysis: {entry_point}")
        
        # Determine if entry point is a notebook or script
        if entry_point.endswith('.ipynb'):
            # Parse the entry point notebook
            executed_scripts = self.parse_notebook(entry_point)
            
            # Queue for files to process
            files_to_process = []
            
            # Process executed scripts from notebook
            for script in executed_scripts:
                print(f"Executes Script: {script}")
                if script not in self.visited_files:
                    files_to_process.append(script)
                    self.visited_files.add(script)
                    
            # Manually add setup.py to the analysis queue since it's downloaded dynamically
            setup_py_path = str(self.repo_root / "scripts" / "setup.py")
            if setup_py_path not in self.visited_files and pathlib.Path(setup_py_path).exists():
                print(f"Manually adding setup.py for analysis: {setup_py_path}")
                files_to_process.append(setup_py_path)
                self.visited_files.add(setup_py_path)
        else:
            # Direct script analysis
            files_to_process = [entry_point]
            self.visited_files.add(entry_point)
            print(f"Direct script analysis: {entry_point}")
        
        # Process Python files recursively
        while files_to_process:
            file_path = files_to_process.pop(0)
            print(f"Parse File: {file_path}")
            
            # Parse the Python file
            file_info = self.parse_python_file(file_path)
            
            # Check imports for additional files to process
            for import_name in file_info['imports']:
                # Try to find the imported file
                import_path = self._find_import_file(import_name, str(pathlib.Path(file_path).parent))
                if import_path:
                    print(f"Discovers Import: {import_name}")
                    if import_path not in self.visited_files:
                        print(f"Queue for Analysis: Add {import_path} to the processing queue.")
                        files_to_process.append(import_path)
                        self.visited_files.add(import_path)
    
    def _find_import_file(self, import_name: str, current_dir: str) -> Optional[str]:
        """Find the file corresponding to an import statement."""
        # Convert import name to potential file path
        parts = import_name.split('.')
        
        # Handle relative imports
        if import_name.startswith('.'):
            # For relative imports, resolve relative to current directory
            rel_path = import_name.lstrip('.').replace('.', '/')
            base_path = pathlib.Path(current_dir)
            for _ in range(len(import_name) - len(import_name.lstrip('.'))):
                base_path = base_path.parent
            
            possibilities = [
                base_path / f"{rel_path}.py",
                base_path / rel_path / "__init__.py"
            ]
        else:
            # For absolute imports, try different possibilities
            possibilities = [
                self.repo_root / f"{import_name.replace('.', '/')}.py",
                pathlib.Path(current_dir) / f"{import_name.replace('.', '/')}.py",
                self.repo_root / "scripts" / f"{import_name.replace('.', '/')}.py",
                self.repo_root / "scripts" / "en" / f"{import_name.replace('.', '/')}.py",
                self.repo_root / "modules" / f"{import_name.replace('.', '/')}.py",
            ]
            
            # Also try __init__.py files
            for i in range(1, len(parts)):
                base_path = '/'.join(parts[:i])
                possibilities.extend([
                    self.repo_root / base_path / "__init__.py",
                    pathlib.Path(current_dir) / base_path / "__init__.py",
                    self.repo_root / "modules" / base_path / "__init__.py"
                ])
        
        for path in possibilities:
            if path.exists():
                return str(path)
        
        return None
    
    def generate_graph_json(self, output_file: str, entry_point: str = "unknown"):
        """Generate the JSON representation of the graph.
        
        Args:
            output_file: Path to the output JSON file
            entry_point: The entry point that was analyzed (for metadata)
        """
        # Convert our graph data to JSON-serializable format
        nodes = list(self.nodes.values())
        edges = self.edges
        
        graph_json = {
            "nodes": nodes,
            "edges": edges,
            "metadata": {
                "total_nodes": len(nodes),
                "total_edges": len(edges),
                "entry_point": entry_point
            }
        }
        
        # Write to file
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(graph_json, f, indent=2, ensure_ascii=False)
        
        print(f"Graph JSON saved to: {output_file}")
        print(f"Total nodes: {len(nodes)}")
        print(f"Total edges: {len(edges)}")


def main():
    """Main function to run the code graph generator."""
    parser = argparse.ArgumentParser(description="Code Graph Generator for sdAIgen")
    parser.add_argument("entry_point", help="The entry point script to analyze (e.g., scripts/en/widgets-en.py or notebook/ScarySingleDocs_EN.ipynb)")
    parser.add_argument("output_file", help="The name of the output JSON file (e.g., code_graph_cell2_widgets.json)")
    args = parser.parse_args()
    
    # Set repository root
    repo_root = "/home/z/my-project/ScarySingleDocs"
    
    # Create the generator
    generator = CodeGraphGenerator(repo_root)
    
    # Analyze the repository
    generator.analyze_repository(args.entry_point)
    
    # Generate the JSON output
    generator.generate_graph_json(args.output_file, args.entry_point)


if __name__ == "__main__":
    main()