const fs = require('fs');
const path = require('path');

const CONTENT_DIR = path.join(__dirname, '..', 'content', 'docs');

function splitFrontmatter(content) {
  const lines = content.split('\n');
  if (lines[0] !== '---') return { frontmatterLines: [], body: content };
  
  let endIdx = -1;
  for (let i = 1; i < lines.length; i++) {
    if (lines[i] === '---') {
      endIdx = i;
      break;
    }
  }
  
  if (endIdx === -1) return { frontmatterLines: [], body: content };
  
  const frontmatterLines = lines.slice(1, endIdx);
  const body = lines.slice(endIdx + 1).join('\n');
  return { frontmatterLines, body };
}

function getFirstHeading(body) {
  const match = body.match(/^#\s+(.+)$/m);
  return match ? match[1].trim() : null;
}

function titleFromFilename(filename) {
  return filename
    .replace(/\.mdx?$/, '')
    .replace(/-/g, ' ')
    .replace(/_/g, ' ')
    .replace(/\b\w/g, c => c.toUpperCase());
}

function removeDocusaurusImports(body) {
  return body
    .split('\n')
    .filter(line => {
      const trimmed = line.trim();
      if (trimmed.startsWith('import ') && trimmed.includes('from ')) {
        if (trimmed.includes("'@site/") || trimmed.includes('"@site/"')) return false;
        if (trimmed.includes("'@theme/") || trimmed.includes('"@theme/"')) return false;
        if (trimmed.includes("'@docusaurus/") || trimmed.includes('"@docusaurus/"')) return false;
        if (trimmed.includes("react-icons")) return false;
      }
      return true;
    })
    .join('\n');
}

function convertAdmonitions(body) {
  const lines = body.split('\n');
  const out = [];
  let inAdmonition = false;
  let admonitionType = '';
  let admonitionTitle = '';
  let buffer = [];

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    const match = line.match(/^:::(\w+)(?:\s+(.*))?$/);
    const endMatch = line.match(/^:::\s*$/);

    if (match) {
      if (inAdmonition) {
        flushAdmonition(out, admonitionType, admonitionTitle, buffer);
      }
      inAdmonition = true;
      admonitionType = match[1];
      admonitionTitle = match[2] || '';
      buffer = [];
      continue;
    }

    if (endMatch && inAdmonition) {
      flushAdmonition(out, admonitionType, admonitionTitle, buffer);
      inAdmonition = false;
      buffer = [];
      continue;
    }

    if (inAdmonition) {
      buffer.push(line);
    } else {
      out.push(line);
    }
  }

  if (inAdmonition) {
    flushAdmonition(out, admonitionType, admonitionTitle, buffer);
  }

  return out.join('\n');
}

function flushAdmonition(out, type, title, buffer) {
  const label = title || type.charAt(0).toUpperCase() + type.slice(1);
  out.push(`> **${label}**`);
  for (const bline of buffer) {
    out.push(`> ${bline}`);
  }
  out.push('');
}

function stripCustomClasses(body) {
  let result = body
    .replace(/\sclassName="[^"]*"/g, '')
    .replace(/\sclassName='[^']*'/g, '')
    .replace(/\sclass="[^"]*"/g, '')
    .replace(/\sclass='[^']*'/g, '');

  result = result.replace(/<[A-Z][a-zA-Z]*\s+[^>]*\/>/g, '');
  result = result.replace(/<[A-Z][a-zA-Z]*\s*\/>/g, '');
  result = result.replace(/<\w+Icon\s+[^>]*\/>/g, '');
  result = result.replace(/<\w+Icon\s*\/>/g, '');
  result = result.replace(/<\w+\/>/g, '');

  result = result.replace(/\sstyle="[^"]*"/g, '');
  result = result.replace(/\sstyle='[^']*'/g, '');
  result = result.replace(/\ssize=\{[^}]*\}/g, '');

  result = result.replace(/<\w+\s+>/g, '<');
  result = result.replace(/<\w+\s+\/>/g, '');

  result = result.replace(/<br\s*\/?>/g, '\n');
  result = result.replace(/<details\s*>/g, '<details>');
  result = result.replace(/<summary\s*>/g, '<summary>');

  result = result.replace(/\n{3,}/g, '\n\n');

  return result;
}

function cleanComponentUsage(body) {
  return body
    .replace(/<\/?NoteBoxs>/g, '')
    .replace(/<\/?InfoBox>/g, '')
    .replace(/<\/?WarningBox>/g, '')
    .replace(/<\/?TipBox>/g, '')
    .replace(/<\/?DangerBox>/g, '')
    .replace(/<\/?SuccessBox>/g, '')
    .replace(/<TutorialCards\s*\/>/g, '')
    .replace(/<!--\s*import\s+.*?\s*-->/g, '')
    .replace(/<!--\s*<\w+\s*\/>\s*-->/g, '');
}

function fixEnvCodeBlocks(body) {
  return body.replace(/```env\n/g, '```bash\n');
}

function processFile(filePath) {
  let content = fs.readFileSync(filePath, 'utf8');
  let { frontmatterLines, body } = splitFrontmatter(content);

  let hasTitle = false;
  for (const line of frontmatterLines) {
    if (line.match(/^title:\s*.+/)) hasTitle = true;
  }

  frontmatterLines = frontmatterLines.filter(line => !line.match(/^sidebar_position:\s*.+/));

  if (!hasTitle) {
    const heading = getFirstHeading(body);
    const filename = path.basename(filePath);
    const derivedTitle = heading || titleFromFilename(filename);
    frontmatterLines.unshift(`title: ${derivedTitle}`);
  }

  body = removeDocusaurusImports(body);
  body = convertAdmonitions(body);
  body = stripCustomClasses(body);
  body = cleanComponentUsage(body);
  body = fixEnvCodeBlocks(body);

  const newFrontmatter = frontmatterLines.length > 0
    ? `---\n${frontmatterLines.join('\n')}\n---\n\n`
    : '';
  const newContent = newFrontmatter + body;
  fs.writeFileSync(filePath, newContent, 'utf8');

  const posMatch = content.match(/sidebar_position:\s*([\d.]+)/);
  const position = posMatch ? parseFloat(posMatch[1]) : Infinity;
  const titleMatch = content.match(/title:\s*(.+)/);
  const title = titleMatch ? titleMatch[1].trim() : (hasTitle ? '' : titleFromFilename(path.basename(filePath)));

  return { slug: path.basename(filePath, path.extname(filePath)), position, title };
}

function getFolderChildren(dir) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  const children = [];
  for (const entry of entries) {
    if (entry.name === 'meta.json') continue;
    if (entry.isDirectory()) {
      children.push({ name: entry.name, type: 'folder' });
    } else if (entry.name.endsWith('.md') || entry.name.endsWith('.mdx')) {
      children.push({ name: entry.name, type: 'file' });
    }
  }
  return children;
}

function generateMetaJson(dir) {
  const children = getFolderChildren(dir);
  const entriesWithPosition = [];

  for (const child of children) {
    const childPath = path.join(dir, child.name);
    let position = Infinity;
    let title = child.name;

    if (child.type === 'file') {
      const content = fs.readFileSync(childPath, 'utf8');
      const posMatch = content.match(/sidebar_position:\s*([\d.]+)/);
      if (posMatch) position = parseFloat(posMatch[1]);
      const titleMatch = content.match(/title:\s*(.+)/);
      if (titleMatch) title = titleMatch[1].trim();
      const slug = child.name.replace(/\.mdx?$/, '');
      entriesWithPosition.push({ slug, position, title, type: 'file' });
    } else {
      const indexPath = path.join(childPath, 'index.md');
      const indexMdxPath = path.join(childPath, 'index.mdx');
      let indexContent = null;
      if (fs.existsSync(indexPath)) indexContent = fs.readFileSync(indexPath, 'utf8');
      else if (fs.existsSync(indexMdxPath)) indexContent = fs.readFileSync(indexMdxPath, 'utf8');

      if (indexContent) {
        const posMatch = indexContent.match(/sidebar_position:\s*([\d.]+)/);
        if (posMatch) position = parseFloat(posMatch[1]);
        const titleMatch = indexContent.match(/title:\s*(.+)/);
        if (titleMatch) title = titleMatch[1].trim();
      }
      entriesWithPosition.push({ slug: child.name, position, title, type: 'folder' });
    }
  }

  entriesWithPosition.sort((a, b) => {
    if (a.position !== b.position) return a.position - b.position;
    return a.title.localeCompare(b.title);
  });

  const pageSlugs = entriesWithPosition.map(e => e.slug);
  const folderTitle = path.basename(dir);

  const indexPath = path.join(dir, 'index.md');
  const indexMdxPath = path.join(dir, 'index.mdx');
  let metaTitle = folderTitle.replace(/-/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
  if (fs.existsSync(indexPath)) {
    const content = fs.readFileSync(indexPath, 'utf8');
    const tmatch = content.match(/title:\s*(.+)/);
    if (tmatch) metaTitle = tmatch[1].trim();
  } else if (fs.existsSync(indexMdxPath)) {
    const content = fs.readFileSync(indexMdxPath, 'utf8');
    const tmatch = content.match(/title:\s*(.+)/);
    if (tmatch) metaTitle = tmatch[1].trim();
  }

  const meta = {
    title: metaTitle,
    pages: pageSlugs,
  };

  fs.writeFileSync(path.join(dir, 'meta.json'), JSON.stringify(meta, null, 2) + '\n', 'utf8');
}

function walkAndGenerateMeta(dir) {
  generateMetaJson(dir);
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const entry of entries) {
    if (entry.isDirectory()) {
      walkAndGenerateMeta(path.join(dir, entry.name));
    }
  }
}

function walkAndProcessFiles(dir) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      walkAndProcessFiles(fullPath);
    } else if (entry.name.endsWith('.md') || entry.name.endsWith('.mdx')) {
      processFile(fullPath);
    }
  }
}

// Main
console.log('Processing content files...');
walkAndProcessFiles(CONTENT_DIR);

console.log('Generating meta.json files...');
walkAndGenerateMeta(CONTENT_DIR);

console.log('Done!');
