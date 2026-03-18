import { useState, useRef, useEffect, useCallback } from "react";

// ─── Utilities ────────────────────────────────────────────────────────────────

function deepEqual(a, b) {
  if (a === b) return true;
  return JSON.stringify(a) === JSON.stringify(b);
}

function serialize(val) {
  if (val === undefined) return "undefined";
  return JSON.stringify(val, null, 2);
}

function runTests(code, functionName, testCases) {
  try {
    const factory = new Function(
      code + `\nreturn typeof ${functionName} !== 'undefined' ? ${functionName} : null;`
    );
    const fn = factory();
    if (!fn)
      return [
        {
          passed: false,
          error: `Function "${functionName}" not found. Make sure you define it with that exact name.`,
          description: "Setup check",
        },
      ];
    return testCases.map((tc) => {
      try {
        const result = fn(...tc.args);
        const passed = deepEqual(result, tc.expected);
        return { passed, result, expected: tc.expected, description: tc.description, error: null };
      } catch (e) {
        return { passed: false, result: null, expected: tc.expected, description: tc.description, error: e.message };
      }
    });
  } catch (e) {
    return [{ passed: false, result: null, expected: null, description: "Syntax / Runtime Error", error: e.message }];
  }
}

// ─── Problem Data ─────────────────────────────────────────────────────────────

const PROBLEMS = [
  // DAY 1
  {
    id: 1, day: 1, title: "Split Path Into Parts",
    description: `Write a function \`splitPath\` that takes a file path string and returns an array of all its parts (folders and filename), with no empty strings.`,
    examples: [
      { input: `"/geology/data/wells/sample.csv"`, output: `["geology", "data", "wells", "sample.csv"]` },
      { input: `"/seismic/gamma.json"`, output: `["seismic", "gamma.json"]` },
    ],
    starterCode: `function splitPath(path) {\n  // your code here\n}`,
    functionName: "splitPath",
    testCases: [
      { args: ["/geology/data/wells/sample.csv"], expected: ["geology","data","wells","sample.csv"], description: "nested path" },
      { args: ["/seismic/gamma.json"], expected: ["seismic","gamma.json"], description: "shallow path" },
      { args: ["/archive/"], expected: ["archive"], description: "trailing slash" },
    ],
    hints: [
      "Use str.split('/') to break the string into an array of parts.",
      "split('/') creates empty strings at the boundaries — use .filter(Boolean) to remove them.",
    ],
    solution: `function splitPath(path) {\n  return path.split('/').filter(Boolean);\n}`,
  },
  {
    id: 2, day: 1, title: "Get Filename From Path",
    description: `Write a function \`getFilename\` that returns just the filename (last segment) from a file path.`,
    examples: [
      { input: `"/geology/data/wells/sample.csv"`, output: `"sample.csv"` },
      { input: `"/archive/delta.csv"`, output: `"delta.csv"` },
    ],
    starterCode: `function getFilename(path) {\n  // your code here\n}`,
    functionName: "getFilename",
    testCases: [
      { args: ["/geology/data/wells/sample.csv"], expected: "sample.csv", description: "nested path" },
      { args: ["/archive/delta.csv"], expected: "delta.csv", description: "shallow path" },
      { args: ["/file.json"], expected: "file.json", description: "root level file" },
    ],
    hints: [
      "Split the path into parts first, then get the last element.",
      "arr.at(-1) is a clean modern way to get the last item. Or use arr[arr.length - 1].",
    ],
    solution: `function getFilename(path) {\n  const parts = path.split('/').filter(Boolean);\n  return parts.at(-1);\n}`,
  },
  {
    id: 3, day: 1, title: "Get File Extension",
    description: `Write a function \`getExtension\` that takes a filename and returns just its extension (without the dot).`,
    examples: [
      { input: `"sample.csv"`, output: `"csv"` },
      { input: `"archive.tar.gz"`, output: `"gz"` },
    ],
    starterCode: `function getExtension(filename) {\n  // your code here\n}`,
    functionName: "getExtension",
    testCases: [
      { args: ["sample.csv"], expected: "csv", description: "csv file" },
      { args: ["data.json"], expected: "json", description: "json file" },
      { args: ["archive.tar.gz"], expected: "gz", description: "double extension — return last" },
    ],
    hints: [
      "Split the filename by '.' — the extension is the last segment.",
      "Array.prototype.pop() removes and returns the last element. Or use .at(-1).",
    ],
    solution: `function getExtension(filename) {\n  return filename.split('.').pop();\n}`,
  },
  {
    id: 4, day: 1, title: "Path Contains Folder",
    description: `Write a function \`pathContainsFolder\` that returns true if a given folder name exists in the path segments — not counting the filename.`,
    examples: [
      { input: `"/geology/data/wells/sample.csv", "data"`, output: `true` },
      { input: `"/geology/data/wells/sample.csv", "archive"`, output: `false` },
      { input: `"/geology/data/wells/sample.csv", "sample.csv"`, output: `false  // filename doesn't count` },
    ],
    starterCode: `function pathContainsFolder(path, folder) {\n  // your code here\n}`,
    functionName: "pathContainsFolder",
    testCases: [
      { args: ["/geology/data/wells/sample.csv", "data"], expected: true, description: "folder exists" },
      { args: ["/geology/data/wells/sample.csv", "archive"], expected: false, description: "folder not in path" },
      { args: ["/geology/data/wells/sample.csv", "sample.csv"], expected: false, description: "filename should not match" },
    ],
    hints: [
      "Split and filter the path into parts. Then remove the last item — that's the filename.",
      "Use slice(0, -1) to get everything except the last element, then check .includes(folder).",
    ],
    solution: `function pathContainsFolder(path, folder) {\n  const parts = path.split('/').filter(Boolean);\n  const folders = parts.slice(0, -1);\n  return folders.includes(folder);\n}`,
  },
  {
    id: 5, day: 1, title: "Replace Folder in Path",
    description: `Write a function \`replaceFolder\` that replaces a folder name in a path with a new name. Only replace folder segments — not the filename.`,
    examples: [
      { input: `"/geology/data/wells/sample.csv", "data", "archive"`, output: `"/geology/archive/wells/sample.csv"` },
    ],
    starterCode: `function replaceFolder(path, oldFolder, newFolder) {\n  // your code here\n}`,
    functionName: "replaceFolder",
    testCases: [
      { args: ["/geology/data/wells/sample.csv", "data", "archive"], expected: "/geology/archive/wells/sample.csv", description: "replaces middle folder" },
      { args: ["/geology/data/wells/sample.csv", "geology", "minerals"], expected: "/minerals/data/wells/sample.csv", description: "replaces first folder" },
      { args: ["/geology/data/wells/sample.csv", "missing", "archive"], expected: "/geology/data/wells/sample.csv", description: "no match — return unchanged" },
    ],
    hints: [
      "Split into parts. Use map() to transform each segment.",
      "Only replace a part if it matches oldFolder AND it's not the last part (filename).",
      "After mapping, join with '/' and add the leading slash back.",
    ],
    solution: `function replaceFolder(path, oldFolder, newFolder) {\n  const parts = path.split('/').filter(Boolean);\n  const replaced = parts.map((part, i) => {\n    if (i < parts.length - 1 && part === oldFolder) return newFolder;\n    return part;\n  });\n  return '/' + replaced.join('/');\n}`,
  },

  // DAY 2
  {
    id: 6, day: 2, title: "Filter Files by Tag",
    description: `Given an array of file objects (each with an id, path, and tags array), write a function \`filterByTag\` that returns only the files that include a given tag.`,
    examples: [
      { input: `files, "geology"`, output: `files where tags includes "geology"` },
    ],
    starterCode: `function filterByTag(files, tag) {\n  // your code here\n}`,
    functionName: "filterByTag",
    testCases: [
      {
        args: [[
          { id: 1, path: "/geology/wells/alpha.csv", tags: ["wells", "geology"] },
          { id: 2, path: "/seismic/raw/data.json", tags: ["seismic", "raw"] },
          { id: 3, path: "/geology/logs/beta.csv", tags: ["logs", "geology"] },
        ], "geology"],
        expected: [
          { id: 1, path: "/geology/wells/alpha.csv", tags: ["wells", "geology"] },
          { id: 3, path: "/geology/logs/beta.csv", tags: ["logs", "geology"] },
        ],
        description: "filter by 'geology'"
      },
      {
        args: [[{ id: 1, path: "/geo/a.csv", tags: ["geology"] }], "archive"],
        expected: [],
        description: "no match — empty array"
      },
    ],
    hints: [
      "Use filter() on the files array.",
      "Each file has a .tags array — use .includes(tag) to check membership.",
    ],
    solution: `function filterByTag(files, tag) {\n  return files.filter(file => file.tags.includes(tag));\n}`,
  },
  {
    id: 7, day: 2, title: "Get All File Paths",
    description: `Write a function \`getAllPaths\` that takes an array of file objects and returns just an array of their paths as strings.`,
    examples: [
      { input: `[{id:1, path:"/geo/a.csv", tags:[...]}, ...]`, output: `["/geo/a.csv", ...]` },
    ],
    starterCode: `function getAllPaths(files) {\n  // your code here\n}`,
    functionName: "getAllPaths",
    testCases: [
      {
        args: [[
          { id: 1, path: "/geology/wells/alpha.csv", tags: ["geology"] },
          { id: 2, path: "/seismic/gamma.json", tags: ["seismic"] },
        ]],
        expected: ["/geology/wells/alpha.csv", "/seismic/gamma.json"],
        description: "extracts paths from file objects"
      },
    ],
    hints: ["Use map() — transform each file object into just its .path string."],
    solution: `function getAllPaths(files) {\n  return files.map(file => file.path);\n}`,
  },
  {
    id: 8, day: 2, title: "Count Files With Tag",
    description: `Write a function \`countByTag\` that returns the number of files that include a given tag.`,
    examples: [
      { input: `files, "geology"`, output: `2` },
    ],
    starterCode: `function countByTag(files, tag) {\n  // your code here\n}`,
    functionName: "countByTag",
    testCases: [
      {
        args: [[
          { id: 1, tags: ["geology", "wells"] },
          { id: 2, tags: ["seismic"] },
          { id: 3, tags: ["geology", "logs"] },
        ], "geology"],
        expected: 2,
        description: "counts matching files"
      },
      { args: [[{ id: 1, tags: ["geology"] }], "archive"], expected: 0, description: "no matches" },
    ],
    hints: [
      "filter() returns an array — you can chain .length on it.",
      "Or use reduce() to accumulate a count.",
    ],
    solution: `function countByTag(files, tag) {\n  return files.filter(file => file.tags.includes(tag)).length;\n}`,
  },
  {
    id: 9, day: 2, title: "Get All Unique Tags",
    description: `Write a function \`getAllUniqueTags\` that returns a flat array of every unique tag that appears across all files — no duplicates.`,
    examples: [
      { input: `files with overlapping tags`, output: `["wells", "geology", "seismic", "raw", "logs"]` },
    ],
    starterCode: `function getAllUniqueTags(files) {\n  // your code here\n}`,
    functionName: "getAllUniqueTags",
    testCases: [
      {
        args: [[
          { tags: ["wells", "geology"] },
          { tags: ["seismic", "raw"] },
          { tags: ["geology", "logs"] },
        ]],
        expected: ["wells", "geology", "seismic", "raw", "logs"],
        description: "unique tags, no duplicates"
      },
    ],
    hints: [
      "Use flatMap(file => file.tags) to get all tags in one flat array (including duplicates).",
      "Wrap in new Set() to remove duplicates, then spread back: [...new Set(allTags)].",
    ],
    solution: `function getAllUniqueTags(files) {\n  const allTags = files.flatMap(file => file.tags);\n  return [...new Set(allTags)];\n}`,
  },

  // DAY 3
  {
    id: 10, day: 3, title: "Extract Tags From Path",
    description: `Write a function \`extractTags\` that takes a file path and returns an array of all folder segments — everything except the filename at the end.`,
    examples: [
      { input: `"/geology/data/wells/alpha.csv"`, output: `["geology", "data", "wells"]` },
      { input: `"/seismic/gamma.json"`, output: `["seismic"]` },
    ],
    starterCode: `function extractTags(path) {\n  // your code here\n}`,
    functionName: "extractTags",
    testCases: [
      { args: ["/geology/data/wells/alpha.csv"], expected: ["geology","data","wells"], description: "nested path" },
      { args: ["/seismic/gamma.json"], expected: ["seismic"], description: "single folder" },
      { args: ["/archive/old/data.csv"], expected: ["archive","old"], description: "two folders" },
    ],
    hints: [
      "Split the path and filter out empty strings.",
      "Remove the last element (filename) using slice(0, -1).",
    ],
    solution: `function extractTags(path) {\n  const parts = path.split('/').filter(Boolean);\n  return parts.slice(0, -1);\n}`,
  },
  {
    id: 11, day: 3, title: "Filter Paths by Tag",
    description: `Write a function \`filterPathsByTag\` that takes an array of path strings and a tag, and returns only the paths that contain that tag as a folder segment.`,
    examples: [
      { input: `paths, "geology"`, output: `["/geology/wells/alpha.csv", "/geology/logs/beta.csv"]` },
    ],
    starterCode: `function filterPathsByTag(paths, tag) {\n  // your code here\n}`,
    functionName: "filterPathsByTag",
    testCases: [
      {
        args: [[
          "/geology/data/wells/alpha.csv",
          "/geology/logs/beta.csv",
          "/seismic/raw/gamma.json",
          "/archive/delta.csv",
        ], "geology"],
        expected: ["/geology/data/wells/alpha.csv", "/geology/logs/beta.csv"],
        description: "filter paths containing 'geology'"
      },
      {
        args: [["/geology/wells/alpha.csv", "/seismic/gamma.json"], "missing"],
        expected: [],
        description: "no matches"
      },
    ],
    hints: [
      "Use filter() on the paths array.",
      "For each path, split into folder parts (no filename) and check .includes(tag).",
      "You can reuse the extractTags logic from the previous problem inside filter.",
    ],
    solution: `function filterPathsByTag(paths, tag) {\n  return paths.filter(path => {\n    const folders = path.split('/').filter(Boolean).slice(0, -1);\n    return folders.includes(tag);\n  });\n}`,
  },
  {
    id: 12, day: 3, title: "Get Unique Top-Level Folders",
    description: `Write a function \`getTopLevelFolders\` that takes an array of file paths and returns the unique top-level folder names (the first folder in each path, deduplicated).`,
    examples: [
      { input: `["/geology/a.csv", "/geology/b.csv", "/seismic/c.json", "/archive/d.csv"]`, output: `["geology", "seismic", "archive"]` },
    ],
    starterCode: `function getTopLevelFolders(paths) {\n  // your code here\n}`,
    functionName: "getTopLevelFolders",
    testCases: [
      {
        args: [["/geology/wells/alpha.csv", "/geology/logs/beta.csv", "/seismic/raw/gamma.json", "/archive/delta.csv"]],
        expected: ["geology", "seismic", "archive"],
        description: "unique top-level folders in order of first appearance"
      },
    ],
    hints: [
      "Map each path to its first folder: path.split('/').filter(Boolean)[0]",
      "Then deduplicate: [...new Set(topFolders)]",
    ],
    solution: `function getTopLevelFolders(paths) {\n  const tops = paths.map(p => p.split('/').filter(Boolean)[0]);\n  return [...new Set(tops)];\n}`,
  },
  {
    id: 13, day: 3, title: "Group Paths by Folder ⭐",
    description: `Write a function \`groupByFolder\` that takes an array of paths and returns an object where each key is a top-level folder and the value is an array of all paths under it.

This is the most important reduce() pattern. Master this one.`,
    examples: [
      { input: `["/geo/a.csv", "/geo/b.csv", "/seismic/c.json"]`, output: `{ geo: ["/geo/a.csv", "/geo/b.csv"], seismic: ["/seismic/c.json"] }` },
    ],
    starterCode: `function groupByFolder(paths) {\n  return paths.reduce((acc, path) => {\n    // 1. get the top-level folder from path\n    // 2. if acc[folder] doesn't exist, initialize as []\n    // 3. push path into acc[folder]\n    // 4. return acc\n  }, {});\n}`,
    functionName: "groupByFolder",
    testCases: [
      {
        args: [["/geology/wells/alpha.csv", "/geology/logs/beta.csv", "/seismic/gamma.json"]],
        expected: {
          geology: ["/geology/wells/alpha.csv", "/geology/logs/beta.csv"],
          seismic: ["/seismic/gamma.json"]
        },
        description: "groups paths by top-level folder"
      },
    ],
    hints: [
      "The starter code already has the reduce() skeleton — fill in the 4 steps.",
      "Get the top folder: path.split('/').filter(Boolean)[0]",
      "Initialize if missing: if (!acc[folder]) acc[folder] = [];",
      "Then: acc[folder].push(path); return acc;",
    ],
    solution: `function groupByFolder(paths) {\n  return paths.reduce((acc, path) => {\n    const folder = path.split('/').filter(Boolean)[0];\n    if (!acc[folder]) acc[folder] = [];\n    acc[folder].push(path);\n    return acc;\n  }, {});\n}`,
  },

  // DAY 4
  {
    id: 14, day: 4, title: "Sum 1 to N (Warmup)",
    description: `Write a recursive function \`sumTo\` that returns the sum of all integers from 1 to n. Do not use a loop or built-in sum functions.

This is a warmup to build the recursive thinking pattern before the harder problems.`,
    examples: [
      { input: `5`, output: `15  // 1+2+3+4+5` },
      { input: `3`, output: `6   // 1+2+3` },
    ],
    starterCode: `function sumTo(n) {\n  // Base case: what's the smallest n where you know the answer?\n  // Recursive case: express sumTo(n) in terms of sumTo(n-1)\n}`,
    functionName: "sumTo",
    testCases: [
      { args: [5], expected: 15, description: "sumTo(5) === 15" },
      { args: [3], expected: 6, description: "sumTo(3) === 6" },
      { args: [1], expected: 1, description: "sumTo(1) === 1 (base case)" },
    ],
    hints: [
      "Base case: if n === 1, return 1.",
      "Recursive case: sumTo(n) = n + sumTo(n-1). That's it.",
    ],
    solution: `function sumTo(n) {\n  if (n === 1) return 1;\n  return n + sumTo(n - 1);\n}`,
  },
  {
    id: 15, day: 4, title: "Count Files in Tree",
    description: `Write a recursive function \`countFiles\` that counts the total number of files across an entire nested folder structure.

Each folder object looks like:
\`{ name: string, files: string[], subfolders: folder[] }\``,
    examples: [
      { input: `folder with 2 files + subfolder with 1 file`, output: `3` },
    ],
    starterCode: `function countFiles(folder) {\n  // 1. Start with this folder's file count\n  // 2. Loop through subfolders and add countFiles(sub) to your count\n  // 3. Return the total\n}`,
    functionName: "countFiles",
    testCases: [
      {
        args: [{
          name: "geology", files: ["alpha.csv", "beta.csv"],
          subfolders: [
            { name: "wells", files: ["gamma.csv"], subfolders: [] },
            { name: "logs", files: ["delta.csv", "epsilon.csv"], subfolders: [
              { name: "archive", files: ["zeta.csv"], subfolders: [] }
            ]},
          ]
        }],
        expected: 6,
        description: "counts all files across 3 levels"
      },
      {
        args: [{ name: "empty", files: [], subfolders: [] }],
        expected: 0,
        description: "empty folder returns 0"
      },
    ],
    hints: [
      "Start with: let count = folder.files.length",
      "Then: for (const sub of folder.subfolders) { count += countFiles(sub); }",
      "Return count.",
    ],
    solution: `function countFiles(folder) {\n  let count = folder.files.length;\n  for (const sub of folder.subfolders) {\n    count += countFiles(sub);\n  }\n  return count;\n}`,
  },
  {
    id: 16, day: 4, title: "Get All Files From Tree",
    description: `Write a recursive function \`getAllFiles\` that returns a flat array of every filename in a nested folder structure.`,
    examples: [
      { input: `folder tree`, output: `["alpha.csv", "beta.csv", "gamma.csv", ...]` },
    ],
    starterCode: `function getAllFiles(folder) {\n  // Collect files from this folder\n  // Then collect from all subfolders recursively\n  // Return them all combined in one flat array\n}`,
    functionName: "getAllFiles",
    testCases: [
      {
        args: [{
          name: "geology", files: ["alpha.csv", "beta.csv"],
          subfolders: [
            { name: "wells", files: ["gamma.csv"], subfolders: [] },
          ]
        }],
        expected: ["alpha.csv", "beta.csv", "gamma.csv"],
        description: "flat list from nested structure"
      },
    ],
    hints: [
      "Start with: let files = [...folder.files]",
      "For each subfolder: files.push(...getAllFiles(sub))",
      "Or use the elegant one-liner: return [...folder.files, ...folder.subfolders.flatMap(getAllFiles)]",
    ],
    solution: `function getAllFiles(folder) {\n  return [\n    ...folder.files,\n    ...folder.subfolders.flatMap(getAllFiles)\n  ];\n}`,
  },
  {
    id: 17, day: 4, title: "Find Folder by Name",
    description: `Write a recursive function \`findFolder\` that searches a nested folder structure and returns the folder object with a matching name. Return null if not found.`,
    examples: [
      { input: `folderTree, "archive"`, output: `{ name: "archive", files: [...], subfolders: [] }` },
      { input: `folderTree, "missing"`, output: `null` },
    ],
    starterCode: `function findFolder(folder, name) {\n  // Base case 1: this folder matches — return it\n  // Base case 2: no subfolders — return null\n  // Recursive case: search each subfolder\n}`,
    functionName: "findFolder",
    testCases: [
      {
        args: [{
          name: "geology", files: [],
          subfolders: [
            { name: "wells", files: [], subfolders: [] },
            { name: "logs", files: [], subfolders: [
              { name: "archive", files: ["old.csv"], subfolders: [] }
            ]},
          ]
        }, "archive"],
        expected: { name: "archive", files: ["old.csv"], subfolders: [] },
        description: "finds deeply nested folder"
      },
      {
        args: [{ name: "geology", files: [], subfolders: [] }, "missing"],
        expected: null,
        description: "returns null when not found"
      },
    ],
    hints: [
      "If folder.name === name, return folder immediately.",
      "Loop through subfolders. Call findFolder(sub, name). If the result isn't null, return it.",
      "If no subfolder found it, return null.",
    ],
    solution: `function findFolder(folder, name) {\n  if (folder.name === name) return folder;\n  for (const sub of folder.subfolders) {\n    const found = findFolder(sub, name);\n    if (found) return found;\n  }\n  return null;\n}`,
  },

  // DAY 5
  {
    id: 18, day: 5, title: "⏱ Add Tag Immutably",
    timed: true, timeLimitSeconds: 900,
    description: `Write a function \`addTag\` that adds a tag to a specific file by id. 

**Critical rule: do not mutate the original array.** Return a brand new array with a new file object for the modified file. This is the immutability pattern React depends on.`,
    examples: [
      { input: `files, id=1, "archive"`, output: `new array — file #1 now has "archive" in tags, others unchanged` },
    ],
    starterCode: `function addTag(files, id, newTag) {\n  // Do NOT mutate the original array or objects\n  // Return a new array\n}`,
    functionName: "addTag",
    testCases: [
      {
        args: [
          [{ id: 1, tags: ["geology", "wells"] }, { id: 2, tags: ["seismic"] }],
          1, "archive"
        ],
        expected: [
          { id: 1, tags: ["geology", "wells", "archive"] },
          { id: 2, tags: ["seismic"] },
        ],
        description: "adds tag to correct file, others unchanged"
      },
      {
        args: [
          [{ id: 1, tags: ["geology"] }, { id: 2, tags: ["seismic"] }],
          2, "raw"
        ],
        expected: [
          { id: 1, tags: ["geology"] },
          { id: 2, tags: ["seismic", "raw"] },
        ],
        description: "adds tag to second file"
      },
    ],
    hints: [
      "Use map() — it always returns a new array without mutating.",
      "For the matching file: return { ...file, tags: [...file.tags, newTag] } — spreads make new objects/arrays.",
      "For non-matching files: return file as-is.",
    ],
    solution: `function addTag(files, id, newTag) {\n  return files.map(file => {\n    if (file.id === id) {\n      return { ...file, tags: [...file.tags, newTag] };\n    }\n    return file;\n  });\n}`,
  },
  {
    id: 19, day: 5, title: "⏱ Build Breadcrumbs",
    timed: true, timeLimitSeconds: 900,
    description: `Write a function \`getBreadcrumbs\` that takes a file path and returns an array of breadcrumb objects — one per path segment — each with a \`label\` and a cumulative \`path\` up to that point.`,
    examples: [
      {
        input: `"/geology/data/wells/sample.csv"`,
        output: `[
  { label: "geology",    path: "/geology" },
  { label: "data",       path: "/geology/data" },
  { label: "wells",      path: "/geology/data/wells" },
  { label: "sample.csv", path: "/geology/data/wells/sample.csv" },
]`
      },
    ],
    starterCode: `function getBreadcrumbs(path) {\n  // Return an array of { label, path } objects\n  // Each path is cumulative up to that segment\n}`,
    functionName: "getBreadcrumbs",
    testCases: [
      {
        args: ["/geology/data/wells/sample.csv"],
        expected: [
          { label: "geology", path: "/geology" },
          { label: "data", path: "/geology/data" },
          { label: "wells", path: "/geology/data/wells" },
          { label: "sample.csv", path: "/geology/data/wells/sample.csv" },
        ],
        description: "4-segment path"
      },
      {
        args: ["/seismic/gamma.json"],
        expected: [
          { label: "seismic", path: "/seismic" },
          { label: "gamma.json", path: "/seismic/gamma.json" },
        ],
        description: "2-segment path"
      },
    ],
    hints: [
      "Split the path and filter empty strings to get the parts array.",
      "Use map() with the index (i) available: parts.map((label, i) => ...)",
      "For each label at index i, the cumulative path is: '/' + parts.slice(0, i + 1).join('/')",
    ],
    solution: `function getBreadcrumbs(path) {\n  const parts = path.split('/').filter(Boolean);\n  return parts.map((label, i) => ({\n    label,\n    path: '/' + parts.slice(0, i + 1).join('/')\n  }));\n}`,
  },
];

const DAY_META = {
  1: { title: "String Methods", color: "#58a6ff" },
  2: { title: "Array Methods", color: "#3fb950" },
  3: { title: "Strings + Arrays", color: "#d2a8ff" },
  4: { title: "Recursion", color: "#ffa657" },
  5: { title: "Timed Practice", color: "#f85149" },
};

// ─── Timer Hook ───────────────────────────────────────────────────────────────

function useTimer(limitSeconds) {
  const [elapsed, setElapsed] = useState(0);
  const [running, setRunning] = useState(false);
  const intervalRef = useRef(null);

  const start = useCallback(() => {
    setElapsed(0);
    setRunning(true);
  }, []);

  const stop = useCallback(() => {
    setRunning(false);
    clearInterval(intervalRef.current);
  }, []);

  const reset = useCallback(() => {
    setElapsed(0);
    setRunning(false);
    clearInterval(intervalRef.current);
  }, []);

  useEffect(() => {
    if (running) {
      intervalRef.current = setInterval(() => setElapsed(e => e + 1), 1000);
    } else {
      clearInterval(intervalRef.current);
    }
    return () => clearInterval(intervalRef.current);
  }, [running]);

  const over = limitSeconds && elapsed >= limitSeconds;
  const remaining = limitSeconds ? Math.max(0, limitSeconds - elapsed) : null;

  return { elapsed, running, over, remaining, start, stop, reset };
}

function formatTime(s) {
  const m = Math.floor(s / 60).toString().padStart(2, "0");
  const sec = (s % 60).toString().padStart(2, "0");
  return `${m}:${sec}`;
}

// ─── Sub-components ───────────────────────────────────────────────────────────

function TestResult({ result }) {
  return (
    <div style={{
      display: "flex", flexDirection: "column", gap: 6,
      padding: "10px 14px",
      background: result.passed ? "rgba(63,185,80,0.07)" : "rgba(248,81,73,0.07)",
      border: `1px solid ${result.passed ? "rgba(63,185,80,0.25)" : "rgba(248,81,73,0.25)"}`,
      borderRadius: 6,
      fontFamily: "monospace",
      fontSize: 12,
    }}>
      <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
        <span style={{ fontSize: 14 }}>{result.passed ? "✅" : "❌"}</span>
        <span style={{ color: "#c9d1d9", fontFamily: "sans-serif", fontSize: 13 }}>
          {result.description}
        </span>
      </div>
      {result.error && (
        <div style={{ color: "#f85149", marginTop: 2 }}>
          <span style={{ color: "#8b949e" }}>Error: </span>{result.error}
        </div>
      )}
      {!result.passed && !result.error && (
        <>
          <div style={{ color: "#8b949e" }}>
            Got: <span style={{ color: "#ffa657" }}>{serialize(result.result)}</span>
          </div>
          <div style={{ color: "#8b949e" }}>
            Expected: <span style={{ color: "#3fb950" }}>{serialize(result.expected)}</span>
          </div>
        </>
      )}
    </div>
  );
}

// ─── Main App ─────────────────────────────────────────────────────────────────

export default function App() {
  const days = [1, 2, 3, 4, 5];
  const [activeDay, setActiveDay] = useState(1);
  const [activeProblemId, setActiveProblemId] = useState(1);
  const [codes, setCodes] = useState(() =>
    Object.fromEntries(PROBLEMS.map(p => [p.id, p.starterCode]))
  );
  const [results, setResults] = useState({});
  const [hintIndex, setHintIndex] = useState({});
  const [showSolution, setShowSolution] = useState({});
  const [solved, setSolved] = useState({});
  const [timerStarted, setTimerStarted] = useState({});
  const textareaRef = useRef(null);

  const problem = PROBLEMS.find(p => p.id === activeProblemId);
  const dayProblems = PROBLEMS.filter(p => p.day === activeDay);
  const meta = DAY_META[activeDay];

  const timer = useTimer(problem?.timed ? problem.timeLimitSeconds : null);

  useEffect(() => {
    if (textareaRef.current) textareaRef.current.focus();
    timer.reset();
    setTimerStarted(ts => ({ ...ts, [activeProblemId]: false }));
  }, [activeProblemId]);

  const handleRun = () => {
    if (!problem) return;
    const code = codes[problem.id];
    const res = runTests(code, problem.functionName, problem.testCases);
    setResults(r => ({ ...r, [problem.id]: res }));
    if (res.every(r => r.passed)) {
      setSolved(s => ({ ...s, [problem.id]: true }));
      if (problem.timed) timer.stop();
    }
  };

  const handleKeyDown = (e) => {
    if ((e.metaKey || e.ctrlKey) && e.key === "Enter") {
      e.preventDefault();
      handleRun();
    }
    if (e.key === "Tab") {
      e.preventDefault();
      const ta = e.target;
      const start = ta.selectionStart;
      const end = ta.selectionEnd;
      const newVal = ta.value.substring(0, start) + "  " + ta.value.substring(end);
      setCodes(c => ({ ...c, [problem.id]: newVal }));
      requestAnimationFrame(() => {
        ta.selectionStart = ta.selectionEnd = start + 2;
      });
    }
  };

  const handleStartTimer = () => {
    timer.start();
    setTimerStarted(ts => ({ ...ts, [activeProblemId]: true }));
  };

  const handleNextHint = () => {
    const cur = hintIndex[problem.id] ?? -1;
    if (cur < problem.hints.length - 1) {
      setHintIndex(h => ({ ...h, [problem.id]: cur + 1 }));
    }
  };

  const totalSolved = Object.values(solved).filter(Boolean).length;
  const currentHintIdx = hintIndex[problem?.id] ?? -1;
  const currentResults = results[problem?.id];
  const allPassed = currentResults?.every(r => r.passed);
  const isSolutionShown = showSolution[problem?.id];

  const timerColor = problem?.timed && timer.remaining !== null
    ? timer.remaining < 120 ? "#f85149"
      : timer.remaining < 300 ? "#ffa657"
      : "#3fb950"
    : "#3fb950";

  return (
    <div style={{
      display: "flex", height: "100vh", overflow: "hidden",
      background: "#0d1117",
      fontFamily: "'Segoe UI', system-ui, sans-serif",
      color: "#c9d1d9",
    }}>

      {/* ── Sidebar ── */}
      <div style={{
        width: 240, minWidth: 240, background: "#010409",
        borderRight: "1px solid #21262d",
        display: "flex", flexDirection: "column", overflow: "hidden",
      }}>
        {/* Header */}
        <div style={{ padding: "16px 16px 12px", borderBottom: "1px solid #21262d" }}>
          <div style={{ fontSize: 11, color: "#58a6ff", letterSpacing: "0.08em", fontWeight: 600, textTransform: "uppercase", marginBottom: 4 }}>
            Kobold Metals Prep
          </div>
          <div style={{ fontSize: 13, color: "#8b949e" }}>
            {totalSolved} / {PROBLEMS.length} solved
          </div>
          <div style={{
            marginTop: 8, height: 4, background: "#21262d", borderRadius: 2, overflow: "hidden"
          }}>
            <div style={{
              height: "100%",
              width: `${(totalSolved / PROBLEMS.length) * 100}%`,
              background: "#58a6ff",
              borderRadius: 2,
              transition: "width 0.3s ease",
            }} />
          </div>
        </div>

        {/* Day Tabs */}
        <div style={{ display: "flex", borderBottom: "1px solid #21262d" }}>
          {days.map(d => {
            const dayCount = PROBLEMS.filter(p => p.day === d).length;
            const dayDone = PROBLEMS.filter(p => p.day === d && solved[p.id]).length;
            const active = d === activeDay;
            return (
              <button key={d}
                onClick={() => {
                  setActiveDay(d);
                  const first = PROBLEMS.find(p => p.day === d);
                  if (first) setActiveProblemId(first.id);
                }}
                style={{
                  flex: 1, padding: "8px 0", border: "none", cursor: "pointer",
                  background: active ? "#161b22" : "transparent",
                  color: active ? DAY_META[d].color : "#8b949e",
                  fontSize: 12, fontWeight: active ? 700 : 400,
                  borderBottom: active ? `2px solid ${DAY_META[d].color}` : "2px solid transparent",
                  transition: "all 0.15s",
                  position: "relative",
                }}
                title={DAY_META[d].title}
              >
                {d}
                {dayDone === dayCount && dayCount > 0 && (
                  <span style={{ position: "absolute", top: 3, right: 3, fontSize: 8 }}>✓</span>
                )}
              </button>
            );
          })}
        </div>

        {/* Day Title */}
        <div style={{
          padding: "10px 14px 8px",
          fontSize: 11, fontWeight: 700, color: meta.color,
          letterSpacing: "0.06em", textTransform: "uppercase",
        }}>
          Day {activeDay} — {meta.title}
        </div>

        {/* Problem List */}
        <div style={{ flex: 1, overflowY: "auto" }}>
          {dayProblems.map(p => {
            const isActive = p.id === activeProblemId;
            const isSolved = solved[p.id];
            return (
              <button key={p.id}
                onClick={() => setActiveProblemId(p.id)}
                style={{
                  width: "100%", padding: "8px 14px",
                  background: isActive ? "#161b22" : "transparent",
                  border: "none", borderLeft: isActive ? `2px solid ${meta.color}` : "2px solid transparent",
                  cursor: "pointer", textAlign: "left",
                  display: "flex", alignItems: "center", gap: 8,
                  transition: "background 0.1s",
                  color: isActive ? "#e6edf3" : "#8b949e",
                  fontSize: 12,
                }}
              >
                <span style={{ fontSize: 14, width: 18, textAlign: "center", flexShrink: 0 }}>
                  {isSolved ? "✅" : "○"}
                </span>
                <span style={{ lineHeight: 1.35 }}>{p.title}</span>
              </button>
            );
          })}
        </div>

        {/* Reset Button */}
        <div style={{ padding: 12, borderTop: "1px solid #21262d" }}>
          <button
            onClick={() => {
              if (!problem) return;
              setCodes(c => ({ ...c, [problem.id]: problem.starterCode }));
              setResults(r => ({ ...r, [problem.id]: null }));
              setShowSolution(s => ({ ...s, [problem.id]: false }));
              setHintIndex(h => ({ ...h, [problem.id]: -1 }));
            }}
            style={{
              width: "100%", padding: "6px 0",
              background: "transparent", border: "1px solid #30363d",
              borderRadius: 6, color: "#8b949e", fontSize: 12, cursor: "pointer",
            }}
          >
            Reset Problem
          </button>
        </div>
      </div>

      {/* ── Main Content ── */}
      {problem && (
        <div style={{ flex: 1, display: "flex", flexDirection: "column", overflow: "hidden" }}>

          {/* Top Bar */}
          <div style={{
            padding: "12px 20px", borderBottom: "1px solid #21262d",
            display: "flex", alignItems: "center", gap: 12,
            background: "#0d1117",
          }}>
            <span style={{
              fontSize: 11, padding: "2px 8px", borderRadius: 12,
              background: meta.color + "22", color: meta.color,
              fontWeight: 600, letterSpacing: "0.05em",
            }}>
              Day {problem.day}
            </span>
            <span style={{ fontSize: 16, fontWeight: 600, color: "#e6edf3" }}>
              {problem.title}
            </span>
            <span style={{ color: "#8b949e", fontSize: 13, marginLeft: "auto" }}>
              {problem.functionName}()
            </span>
            {problem.timed && (
              <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
                {!timerStarted[activeProblemId] ? (
                  <button onClick={handleStartTimer} style={{
                    padding: "4px 12px", background: "#21262d", border: "1px solid #30363d",
                    borderRadius: 6, color: "#c9d1d9", fontSize: 12, cursor: "pointer",
                  }}>
                    ▶ Start Timer
                  </button>
                ) : (
                  <span style={{
                    fontFamily: "monospace", fontSize: 14, fontWeight: 700,
                    color: timerColor,
                    padding: "2px 10px", background: timerColor + "18",
                    borderRadius: 6, border: `1px solid ${timerColor}40`,
                  }}>
                    {formatTime(timer.remaining ?? 0)}
                  </span>
                )}
              </div>
            )}
          </div>

          {/* Split: left=problem+editor, right=examples+results */}
          <div style={{ flex: 1, display: "flex", overflow: "hidden" }}>

            {/* Left: Editor */}
            <div style={{ flex: 1, display: "flex", flexDirection: "column", overflow: "hidden", borderRight: "1px solid #21262d" }}>
              {/* Description */}
              <div style={{
                padding: "16px 20px",
                borderBottom: "1px solid #21262d",
                fontSize: 13, lineHeight: 1.65, color: "#c9d1d9",
                maxHeight: 160, overflowY: "auto",
                background: "#0d1117",
                whiteSpace: "pre-wrap",
              }}>
                {problem.description}
              </div>

              {/* Editor */}
              <div style={{ flex: 1, display: "flex", flexDirection: "column", padding: "0 0 0 0", overflow: "hidden" }}>
                <div style={{
                  padding: "8px 20px 6px",
                  display: "flex", alignItems: "center", gap: 8,
                  background: "#161b22", borderBottom: "1px solid #21262d",
                }}>
                  <span style={{ fontSize: 11, color: "#8b949e" }}>JavaScript</span>
                  <span style={{ marginLeft: "auto", fontSize: 11, color: "#8b949e" }}>
                    Cmd+Enter to run
                  </span>
                </div>
                <textarea
                  ref={textareaRef}
                  value={codes[problem.id]}
                  onChange={e => setCodes(c => ({ ...c, [problem.id]: e.target.value }))}
                  onKeyDown={handleKeyDown}
                  spellCheck={false}
                  style={{
                    flex: 1, resize: "none", outline: "none", border: "none",
                    background: "#161b22",
                    color: "#c9d1d9",
                    fontFamily: "'Courier New', 'Consolas', monospace",
                    fontSize: 13, lineHeight: 1.7,
                    padding: "14px 20px",
                    tabSize: 2,
                  }}
                />
              </div>

              {/* Run Button */}
              <div style={{
                padding: "12px 20px",
                background: "#161b22",
                borderTop: "1px solid #21262d",
                display: "flex", gap: 10, alignItems: "center",
              }}>
                <button onClick={handleRun} style={{
                  padding: "8px 24px",
                  background: "#238636", border: "1px solid #2ea043",
                  borderRadius: 6, color: "#fff", fontSize: 13, fontWeight: 600,
                  cursor: "pointer", letterSpacing: "0.02em",
                }}>
                  ▶ Run Tests
                </button>
                {allPassed && (
                  <span style={{ fontSize: 13, color: "#3fb950", fontWeight: 600 }}>
                    All tests passing! 🎉
                  </span>
                )}
                {currentResults && !allPassed && (
                  <span style={{ fontSize: 13, color: "#f85149" }}>
                    {currentResults.filter(r => !r.passed).length} test{currentResults.filter(r => !r.passed).length > 1 ? "s" : ""} failing
                  </span>
                )}
              </div>
            </div>

            {/* Right: Examples + Tests + Hints + Solution */}
            <div style={{ width: 380, minWidth: 380, display: "flex", flexDirection: "column", overflow: "hidden", background: "#0d1117" }}>
              <div style={{ flex: 1, overflowY: "auto", padding: "16px" }}>

                {/* Examples */}
                <div style={{ marginBottom: 16 }}>
                  <div style={{ fontSize: 11, color: "#8b949e", textTransform: "uppercase", letterSpacing: "0.06em", marginBottom: 8, fontWeight: 600 }}>
                    Examples
                  </div>
                  {problem.examples.map((ex, i) => (
                    <div key={i} style={{
                      background: "#161b22", borderRadius: 6, padding: "10px 12px",
                      marginBottom: 8, fontSize: 12, fontFamily: "monospace",
                      border: "1px solid #21262d",
                    }}>
                      <div><span style={{ color: "#8b949e" }}>Input:  </span><span style={{ color: "#79c0ff" }}>{ex.input}</span></div>
                      <div><span style={{ color: "#8b949e" }}>Output: </span><span style={{ color: "#3fb950" }}>{ex.output}</span></div>
                    </div>
                  ))}
                </div>

                {/* Test Results */}
                {currentResults && (
                  <div style={{ marginBottom: 16 }}>
                    <div style={{ fontSize: 11, color: "#8b949e", textTransform: "uppercase", letterSpacing: "0.06em", marginBottom: 8, fontWeight: 600 }}>
                      Test Results
                    </div>
                    <div style={{ display: "flex", flexDirection: "column", gap: 6 }}>
                      {currentResults.map((r, i) => <TestResult key={i} result={r} />)}
                    </div>
                  </div>
                )}

                {/* Hints */}
                <div style={{ marginBottom: 16 }}>
                  <div style={{ fontSize: 11, color: "#8b949e", textTransform: "uppercase", letterSpacing: "0.06em", marginBottom: 8, fontWeight: 600 }}>
                    Hints ({currentHintIdx + 1}/{problem.hints.length})
                  </div>
                  {problem.hints.slice(0, currentHintIdx + 1).map((hint, i) => (
                    <div key={i} style={{
                      background: "#161b22", border: "1px solid #ffa65730",
                      borderRadius: 6, padding: "8px 12px",
                      fontSize: 12, color: "#c9d1d9", marginBottom: 6,
                      lineHeight: 1.5,
                    }}>
                      <span style={{ color: "#ffa657", marginRight: 6 }}>💡</span>
                      {hint}
                    </div>
                  ))}
                  {currentHintIdx < problem.hints.length - 1 && (
                    <button onClick={handleNextHint} style={{
                      background: "transparent", border: "1px solid #30363d",
                      borderRadius: 6, color: "#8b949e", fontSize: 12,
                      padding: "5px 12px", cursor: "pointer", width: "100%",
                    }}>
                      + Show next hint
                    </button>
                  )}
                </div>

                {/* Solution */}
                <div>
                  <div style={{ fontSize: 11, color: "#8b949e", textTransform: "uppercase", letterSpacing: "0.06em", marginBottom: 8, fontWeight: 600 }}>
                    Solution
                  </div>
                  {!isSolutionShown ? (
                    <button
                      onClick={() => setShowSolution(s => ({ ...s, [problem.id]: true }))}
                      style={{
                        background: "transparent", border: "1px solid #30363d",
                        borderRadius: 6, color: "#8b949e", fontSize: 12,
                        padding: "6px 12px", cursor: "pointer", width: "100%",
                      }}
                    >
                      Reveal solution
                    </button>
                  ) : (
                    <pre style={{
                      background: "#161b22", border: "1px solid #21262d",
                      borderRadius: 6, padding: "12px",
                      fontSize: 12, fontFamily: "monospace", color: "#a5d6ff",
                      margin: 0, whiteSpace: "pre-wrap", overflowX: "auto",
                      lineHeight: 1.6,
                    }}>
                      {problem.solution}
                    </pre>
                  )}
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}