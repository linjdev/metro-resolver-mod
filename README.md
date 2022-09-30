# metro-resolver-mod
add import ~/ as $root/src/ for metro

```javascript
// src/a/b/c/Page.jsx import src/components/Component.jsx
import Component from '../../../components/Component' --> import Component from '~/components/Component'
```

modify file `node_modules/metro-resolver/src/resolve.js`

### Step 1

Replace

```javascript
function isRelativeImport(filePath)
```

As

```javascript
function isProjectRootSrcPath(filePath) {
  return /^~(?:[/]|$)/.test(filePath)
}

function isRelativeImport(filePath)
```

### Step 2

Replace

```javascript
  if (isRelativeImport(moduleName) || isAbsolutePath(moduleName)) {
```

As

```javascript
  if (isProjectRootSrcPath(moduleName) || isRelativeImport(moduleName) || isAbsolutePath(moduleName)) {
```

### Step 3

Location

```javascript
function resolveModulePath(context, toModuleName, platform)
```

Replace

```javascript
  const modulePath = isAbsolutePath(toModuleName)
    ? resolveWindowsPath(toModuleName)
    : path.join(path.dirname(context.originModulePath), toModuleName);
```

As

```javascript
  const modulePath = isAbsolutePath(toModuleName)
    ? resolveWindowsPath(toModuleName)
    : (
    	isProjectRootSrcPath(toModuleName)
    	? path.join(context.projectRoot, toModuleName.replace(/^~[/]?/, 'src/'))
    	: path.join(path.dirname(context.originModulePath), toModuleName)
    );
```
