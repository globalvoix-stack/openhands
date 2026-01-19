import os
import re
import unittest


class TestCircularImports(unittest.TestCase):
    """Test to detect circular imports in the codebase."""

    def test_no_circular_imports_in_key_modules(self):
        """
        Test that there are no circular imports in key modules that were previously problematic.

        This test specifically checks the modules that were involved in a previous circular import issue:
        - thinksoft.utils.prompt
        - thinksoft.agenthub.codeact_agent.tools.bash
        - thinksoft.agenthub.codeact_agent.tools.prompt
        - thinksoft.memory.memory
        - thinksoft.memory.conversation_memory
        """
        # Get the project root directory
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))

        # Map module names to file paths
        module_paths = {
            'thinksoft.utils.prompt': os.path.join(
                project_root, 'thinksoft/utils/prompt.py'
            ),
            'thinksoft.agenthub.codeact_agent.tools.bash': os.path.join(
                project_root, 'thinksoft/agenthub/codeact_agent/tools/bash.py'
            ),
            'thinksoft.agenthub.codeact_agent.tools.prompt': os.path.join(
                project_root, 'thinksoft/agenthub/codeact_agent/tools/prompt.py'
            ),
            'thinksoft.memory.memory': os.path.join(
                project_root, 'thinksoft/memory/memory.py'
            ),
            'thinksoft.memory.conversation_memory': os.path.join(
                project_root, 'thinksoft/memory/conversation_memory.py'
            ),
        }

        # Check for the specific circular import pattern that was problematic
        circular_imports = self._find_circular_imports(module_paths)

        # If there are any circular imports, fail the test
        if circular_imports:
            circular_import_str = '\n'.join(
                [
                    f'{module1} -> {module2} -> {module1}'
                    for module1, module2 in circular_imports
                ]
            )
            self.fail(f'Circular imports detected:\n{circular_import_str}')

    def _find_circular_imports(
        self, module_paths: dict[str, str]
    ) -> list[tuple[str, str]]:
        """
        Find circular imports between modules.

        Args:
            module_paths: Dictionary mapping module names to file paths

        Returns:
            List of tuples (module1, module2) where module1 imports module2 and module2 imports module1
        """
        # Dictionary to store imports for each module
        module_imports = {}

        # Extract imports for each module
        for module_name, file_path in module_paths.items():
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    source_code = f.read()

                # Extract import statements
                import_lines = [
                    line.strip()
                    for line in source_code.split('\n')
                    if line.strip().startswith(('import ', 'from '))
                    and not line.strip().startswith('# ')
                ]

                # Parse import statements to get imported modules
                imported_modules = []
                for line in import_lines:
                    if line.startswith('import '):
                        # Handle "import module" or "import module as alias"
                        parts = line[7:].split(',')
                        for part in parts:
                            module_part = part.strip().split(' as ')[0].strip()
                            if module_part.startswith('thinksoft.'):
                                imported_modules.append(module_part)
                    elif line.startswith('from '):
                        # Handle "from module import name" or "from module import name as alias"
                        module_part = line[5:].split(' import ')[0].strip()
                        if module_part.startswith('thinksoft.'):
                            imported_modules.append(module_part)

                module_imports[module_name] = imported_modules

        # Check for circular imports
        circular_imports = []
        for module1, imports1 in module_imports.items():
            for module2 in imports1:
                if module2 in module_imports and module1 in module_imports[module2]:
                    # Found a circular import
                    circular_imports.append((module1, module2))

        return circular_imports

    def test_specific_circular_import_pattern(self):
        """
        Test for the specific circular import pattern that caused the issue in the stack trace.

        The problematic pattern was:
        thinksoft.utils.prompt imports from thinksoft.agenthub.codeact_agent.tools.bash
        thinksoft.agenthub.codeact_agent.tools.bash imports from thinksoft.agenthub.codeact_agent.tools.prompt
        thinksoft.agenthub.codeact_agent.tools.prompt imports from thinksoft.utils.prompt
        """
        # Get the project root directory
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))

        # Check if the problematic pattern exists
        prompt_path = os.path.join(project_root, 'thinksoft/utils/prompt.py')
        bash_path = os.path.join(
            project_root, 'thinksoft/agenthub/codeact_agent/tools/bash.py'
        )
        tools_prompt_path = os.path.join(
            project_root, 'thinksoft/agenthub/codeact_agent/tools/prompt.py'
        )

        # Check if all files exist
        if not all(
            os.path.exists(path) for path in [prompt_path, bash_path, tools_prompt_path]
        ):
            self.skipTest('One or more required files do not exist')

        # Read the files
        with open(prompt_path, 'r') as f:
            prompt_code = f.read()

        with open(bash_path, 'r') as f:
            bash_code = f.read()

        with open(tools_prompt_path, 'r') as f:
            tools_prompt_code = f.read()

        # Check for the problematic imports
        prompt_imports_bash = (
            re.search(
                r'from thinksoft\.agenthub\.codeact_agent\.tools\.bash import',
                prompt_code,
            )
            is not None
        )
        bash_imports_tools_prompt = (
            re.search(
                r'from thinksoft\.agenthub\.codeact_agent\.tools\.prompt import',
                bash_code,
            )
            is not None
        )
        tools_prompt_imports_prompt = (
            re.search(r'from thinksoft\.utils\.prompt import', tools_prompt_code)
            is not None
        )

        # If all three imports exist, we have a circular import
        if (
            prompt_imports_bash
            and bash_imports_tools_prompt
            and tools_prompt_imports_prompt
        ):
            self.fail(
                'Circular import pattern detected:\n'
                'thinksoft.utils.prompt imports from thinksoft.agenthub.codeact_agent.tools.bash\n'
                'thinksoft.agenthub.codeact_agent.tools.bash imports from thinksoft.agenthub.codeact_agent.tools.prompt\n'
                'thinksoft.agenthub.codeact_agent.tools.prompt imports from thinksoft.utils.prompt'
            )

    def test_detect_circular_imports_in_server_modules(self):
        """
        Test for circular imports in the server modules that were involved in the stack trace.

        The problematic modules were:
        - thinksoft.server.shared
        - thinksoft.server.conversation_manager.conversation_manager
        - thinksoft.server.session.agent_session
        - thinksoft.server.session
        - thinksoft.server.session.session
        """
        # Get the project root directory
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))

        # Map module names to file paths
        module_paths = {
            'thinksoft.server.shared': os.path.join(
                project_root, 'thinksoft/server/shared.py'
            ),
            'thinksoft.server.conversation_manager.conversation_manager': os.path.join(
                project_root,
                'thinksoft/server/conversation_manager/conversation_manager.py',
            ),
            'thinksoft.server.session.agent_session': os.path.join(
                project_root, 'thinksoft/server/session/agent_session.py'
            ),
            'thinksoft.server.session.__init__': os.path.join(
                project_root, 'thinksoft/server/session/__init__.py'
            ),
            'thinksoft.server.session.session': os.path.join(
                project_root, 'thinksoft/server/session/session.py'
            ),
        }

        # Check for circular imports
        circular_imports = self._find_circular_imports(module_paths)

        # If there are any circular imports, fail the test
        if circular_imports:
            circular_import_str = '\n'.join(
                [
                    f'{module1} -> {module2} -> {module1}'
                    for module1, module2 in circular_imports
                ]
            )
            self.fail(
                f'Circular imports detected in server modules:\n{circular_import_str}'
            )

    def test_detect_circular_imports_in_mcp_modules(self):
        """
        Test for circular imports in the MCP modules that were involved in the stack trace.

        The problematic modules were:
        - thinksoft.mcp
        - thinksoft.mcp.utils
        - thinksoft.memory.memory
        """
        # Get the project root directory
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))

        # Map module names to file paths
        module_paths = {
            'thinksoft.mcp.__init__': os.path.join(
                project_root, 'thinksoft/mcp/__init__.py'
            ),
            'thinksoft.mcp.utils': os.path.join(project_root, 'thinksoft/mcp/utils.py'),
            'thinksoft.memory.memory': os.path.join(
                project_root, 'thinksoft/memory/memory.py'
            ),
        }

        # Check for circular imports
        circular_imports = self._find_circular_imports(module_paths)

        # If there are any circular imports, fail the test
        if circular_imports:
            circular_import_str = '\n'.join(
                [
                    f'{module1} -> {module2} -> {module1}'
                    for module1, module2 in circular_imports
                ]
            )
            self.fail(
                f'Circular imports detected in MCP modules:\n{circular_import_str}'
            )

    def test_detect_complex_circular_import_chains(self):
        """
        Test for complex circular import chains involving multiple modules.

        This test checks for circular dependencies that involve more than two modules,
        such as A imports B, B imports C, and C imports A.
        """
        # Get the project root directory
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))

        # Define the modules involved in the stack trace
        modules = [
            'thinksoft.utils.prompt',
            'thinksoft.agenthub.codeact_agent.tools.bash',
            'thinksoft.agenthub.codeact_agent.tools.prompt',
            'thinksoft.memory.memory',
            'thinksoft.memory.conversation_memory',
            'thinksoft.server.shared',
            'thinksoft.server.conversation_manager.conversation_manager',
            'thinksoft.server.session.agent_session',
            'thinksoft.server.session.__init__',
            'thinksoft.server.session.session',
            'thinksoft.mcp.__init__',
            'thinksoft.mcp.utils',
        ]

        # Map module names to file paths
        module_paths = {}
        for module in modules:
            if module.endswith('.__init__'):
                # Handle __init__.py files
                module_path = module[:-9].replace('.', '/')
                file_path = os.path.join(project_root, f'{module_path}/__init__.py')
            else:
                # Handle regular .py files
                module_path = module.replace('.', '/')
                file_path = os.path.join(project_root, f'{module_path}.py')

            if os.path.exists(file_path):
                module_paths[module] = file_path

        # Build the import graph
        import_graph = {}
        for module_name, file_path in module_paths.items():
            with open(file_path, 'r') as f:
                source_code = f.read()

            # Extract import statements
            import_lines = [
                line.strip()
                for line in source_code.split('\n')
                if line.strip().startswith(('import ', 'from '))
                and not line.strip().startswith('# ')
            ]

            # Parse import statements to get imported modules
            imported_modules = []
            for line in import_lines:
                if line.startswith('import '):
                    # Handle "import module" or "import module as alias"
                    parts = line[7:].split(',')
                    for part in parts:
                        module_part = part.strip().split(' as ')[0].strip()
                        if module_part.startswith('thinksoft.'):
                            imported_modules.append(module_part)
                elif line.startswith('from '):
                    # Handle "from module import name" or "from module import name as alias"
                    module_part = line[5:].split(' import ')[0].strip()
                    if module_part.startswith('thinksoft.'):
                        imported_modules.append(module_part)

            import_graph[module_name] = [
                m for m in imported_modules if m in module_paths
            ]

        # Check for circular import chains
        circular_chains = self._find_circular_chains(import_graph)

        # If there are any circular chains, fail the test
        if circular_chains:
            circular_chain_str = '\n'.join(
                [' -> '.join(chain) for chain in circular_chains]
            )
            self.fail(f'Complex circular import chains detected:\n{circular_chain_str}')

    def _find_circular_chains(
        self, import_graph: dict[str, list[str]]
    ) -> list[list[str]]:
        """
        Find circular import chains in the import graph.

        Args:
            import_graph: Dictionary mapping module names to lists of imported modules

        Returns:
            List of circular import chains, where each chain is a list of module names
        """
        circular_chains = []

        def dfs(module: str, path: list[str], visited: set[str]):
            """
            Depth-first search to find circular import chains.

            Args:
                module: Current module being visited
                path: Current path in the DFS
                visited: Set of modules visited in the current DFS path
            """
            if module in visited:
                # Found a circular import chain
                cycle_start = path.index(module)
                circular_chains.append(path[cycle_start:] + [module])
                return

            visited.add(module)
            path.append(module)

            for imported_module in import_graph.get(module, []):
                dfs(imported_module, path.copy(), visited.copy())

        # Start DFS from each module
        for module in import_graph:
            dfs(module, [], set())

        return circular_chains


if __name__ == '__main__':
    unittest.main()
