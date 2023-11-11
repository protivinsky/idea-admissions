def css_base(max_width=None):
    return f"""
body {{
  font-family: "Libre Franklin", sans-serif;
  color: #444;
  font-size: 90%;
  font-weight: 300;
}}

.container {{
  max-width: {max_width or 1900}px; /* Default max-width */
  margin: 0;
  padding: 20px;
}}

.container.full-width {{
  max-width: none; /* Remove max-width for full-width display */
}}

b, strong {{
  font-weight: 600;
}}

code {{
  font-size: 120%;
  background-color: #f5f5f5;
  border-radius: 5px;
  padding: 12px;
  margin-bottom: 6px;
  display: block;
  width: auto;
  white-space: pre-wrap;
}}

.color_table td, .color_table th {{
    padding: 8px
}}
"""


js_doc_tree_script = """
function hideSiblings(contentId) {
  var contentElement = document.getElementById(contentId);
  var parentElement = contentElement.parentElement;
  var siblingElements = parentElement.children;

  for (var i = 0; i < siblingElements.length; i++) {
    if (siblingElements[i] !== contentElement && siblingElements[i].className === 'content') {
      siblingElements[i].style.display = "none";
    }
  }
}

function showContentAndParents(contentId) {
  // Display the content
  var content = document.getElementById(contentId);
  content.style.display = "block";

  // Hide sibling contents
  hideSiblings(contentId);

  // Recursively display the parent
  var parentContent = content.parentElement.closest('.content');
  if (parentContent) {
    showContentAndParents(parentContent.id);
  }
}

function getFirstChildId(contentId) {
  for (var buttonId in buttonHierarchy) {
    if (buttonHierarchy[buttonId].id === contentId) {
      return buttonHierarchy[buttonId].firstChildId;
    } else {
      for (var childButtonId in buttonHierarchy[buttonId].children) {
        if (buttonHierarchy[buttonId].children[childButtonId].id === contentId) {
          return buttonHierarchy[buttonId].children[childButtonId].firstChildId;
        }
      }
    }
  }
  return null;
}


function showContentAndFirstChild(contentId) {
  // Display the content and its parents
  showContentAndParents(contentId);

  // Recursively display the first child and its descendants
  var firstChildId = getFirstChildId(contentId);
  if (firstChildId) {
    showContentAndFirstChild(firstChildId);
  }
}

function attachHandler(button, contentId) {
  button.addEventListener("click", function() {
    showContentAndFirstChild(contentId);
  });
}

function attachHandlers(buttons) {
  for (var buttonId in buttons) {
    var button = document.getElementById(buttonId);
    var contentId = buttons[buttonId].id;
    attachHandler(button, contentId);

    if (Object.keys(buttons[buttonId].children).length > 0) {
      attachHandlers(buttons[buttonId].children);
    }
  }
}

attachHandlers(buttonHierarchy);
showContentAndFirstChild('page_1');  // Display "page_1" and its first child when the page loads
"""
