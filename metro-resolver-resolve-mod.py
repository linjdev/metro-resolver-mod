#!python3

with open('node_modules/metro-resolver/src/resolve.js', 'r') as rfile:
	content = rfile.read()
	rfile.close()

	if content.find('function isProjectRootSrcPath') == -1:
		content = content.replace('''function isRelativeImport(filePath)''', '''function isProjectRootSrcPath(filePath) {
  return /^~(?:[/]|$)/.test(filePath)
}

function isRelativeImport(filePath)''').replace('''  if (isRelativeImport(moduleName) || isAbsolutePath(moduleName)) {''', '''  if (isProjectRootSrcPath(moduleName) || isRelativeImport(moduleName) || isAbsolutePath(moduleName)) {''').replace('''  const modulePath = isAbsolutePath(toModuleName)
    ? resolveWindowsPath(toModuleName)
    : path.join(path.dirname(context.originModulePath), toModuleName);''', '''  const modulePath = isAbsolutePath(toModuleName)
    ? resolveWindowsPath(toModuleName)
    : (
      isProjectRootSrcPath(toModuleName)
      ? path.join(context.projectRoot, toModuleName.replace(/^~[/]?/, 'src/'))
      : path.join(path.dirname(context.originModulePath), toModuleName)
    );''')
		with open('node_modules/metro-resolver/src/resolve.js', 'w') as wfile:
			wfile.write(content)
			wfile.close()
