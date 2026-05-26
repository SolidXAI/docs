const fs = require('fs');
const path = require('path');

const CONTENT_DIR = path.join(__dirname, '..', 'content', 'docs');

function walkDir(dir) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  const files = [];
  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      files.push(...walkDir(fullPath));
    } else if (entry.name.endsWith('.md') || entry.name.endsWith('.mdx')) {
      files.push(fullPath);
    }
  }
  return files;
}

function fixFile(filePath) {
  let content = fs.readFileSync(filePath, 'utf8');
  let changed = false;

  // Remove HTML comments (they cause "raw" node issues in MDX)
  const noComments = content.replace(/<!--[\s\S]*?-->/g, '');
  if (noComments !== content) {
    content = noComments;
    changed = true;
  }

  // Replace <summary><strong>...</strong></summary> with <summary>...</summary>
  // Replace <code>...</code> inside summary with backtick inline code
  const noStrongSummary = content.replace(
    /<summary>\s*<strong>([\s\S]*?)<\/strong>\s*<\/summary>/g,
    (_, inner) => {
      // Convert <code>x</code> to `x`
      const cleaned = inner.replace(/<code>([\s\S]*?)<\/code>/g, '`$1`');
      return `<summary>${cleaned}</summary>`;
    }
  );
  if (noStrongSummary !== content) {
    content = noStrongSummary;
    changed = true;
  }

  // Replace any remaining <code> inside <summary> with backtick inline code
  const noCodeSummary = content.replace(
    /(<summary>[\s\S]*?)<code>([\s\S]*?)<\/code>([\s\S]*?<\/summary>)/g,
    '$1`$2`$3'
  );
  if (noCodeSummary !== content) {
    content = noCodeSummary;
    changed = true;
  }

  // Replace standalone <code>...</code> in body text (not inside code blocks) with backtick inline code
  // Only do this for simple single-line code tags
  let inCodeBlock = false;
  const lines = content.split('\n');
  const fixedLines = lines.map(line => {
    if (line.trim().startsWith('```')) {
      inCodeBlock = !inCodeBlock;
      return line;
    }
    if (inCodeBlock) return line;
    
    // Replace <code>simple text</code> with `simple text` outside code blocks
    return line.replace(/<code>([^<\n]+?)<\/code>/g, '`$1`');
  });
  const noCodeTags = fixedLines.join('\n');
  if (noCodeTags !== content) {
    content = noCodeTags;
    changed = true;
  }

  // Clean multiple consecutive empty lines
  const cleaned = content.replace(/\n{3,}/g, '\n\n');
  if (cleaned !== content) {
    content = cleaned;
    changed = true;
  }

  if (changed) {
    fs.writeFileSync(filePath, content, 'utf8');
  }
  return changed;
}

const files = walkDir(CONTENT_DIR);
let fixedCount = 0;
for (const file of files) {
  if (fixFile(file)) fixedCount++;
}
console.log(`Fixed ${fixedCount} of ${files.length} files`);
