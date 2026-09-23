import re

with open('frontend/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Add tailwind config
html = html.replace('<script src="https://cdn.tailwindcss.com"></script>', 
                    '<script src="https://cdn.tailwindcss.com"></script>\n    <script>tailwind.config = { darkMode: "class" }</script>')

# Map light classes to include dark classes
replacements = {
    'bg-gray-50 ': 'bg-gray-50 dark:bg-gray-900 ',
    'bg-gray-50"': 'bg-gray-50 dark:bg-gray-900"',
    'bg-white ': 'bg-white dark:bg-gray-800 ',
    'bg-white"': 'bg-white dark:bg-gray-800"',
    'border-gray-200 ': 'border-gray-200 dark:border-gray-700 ',
    'border-gray-200"': 'border-gray-200 dark:border-gray-700"',
    'border-gray-100 ': 'border-gray-100 dark:border-gray-700 ',
    'border-gray-100"': 'border-gray-100 dark:border-gray-700"',
    'text-gray-800 ': 'text-gray-800 dark:text-gray-100 ',
    'text-gray-800"': 'text-gray-800 dark:text-gray-100"',
    'text-gray-700 ': 'text-gray-700 dark:text-gray-200 ',
    'text-gray-700"': 'text-gray-700 dark:text-gray-200"',
    'text-gray-600 ': 'text-gray-600 dark:text-gray-300 ',
    'text-gray-600"': 'text-gray-600 dark:text-gray-300"',
    'text-gray-500 ': 'text-gray-500 dark:text-gray-400 ',
    'text-gray-500"': 'text-gray-500 dark:text-gray-400"',
    'border-gray-300 ': 'border-gray-300 dark:border-gray-600 ',
    'border-gray-300"': 'border-gray-300 dark:border-gray-600"'
}

for old, new in replacements.items():
    html = html.replace(old, new)

# Insert Theme Toggle Button into Sidebar
toggle_btn = '''
        <div class="p-4 border-t border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-900">
            <button onclick="toggleDarkMode()" class="w-full mb-3 py-2 bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-200 rounded-md hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors text-sm font-medium shadow-sm flex items-center justify-center gap-2">
                <svg class="w-4 h-4 dark:hidden" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"></path></svg>
                <svg class="w-4 h-4 hidden dark:block" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"></path></svg>
                Toggle Theme
            </button>
'''
html = html.replace('<div class="p-4 border-t border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-900">', toggle_btn)

# Add Toggle JS logic
js_logic = '''
        // --- Theme Logic ---
        function toggleDarkMode() {
            document.documentElement.classList.toggle('dark');
            localStorage.setItem('theme', document.documentElement.classList.contains('dark') ? 'dark' : 'light');
        }
        if (localStorage.theme === 'dark' || (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
            document.documentElement.classList.add('dark');
        } else {
            document.documentElement.classList.remove('dark');
        }

        // --- Navigation ---
'''
html = html.replace('// --- Navigation ---', js_logic)

with open('frontend/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
