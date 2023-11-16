// This code handle the switching with tabs for Switcher class

function hideSiblings(contentId) {
  var contentElement = document.getElementById(contentId);
  var parentElement = contentElement.parentElement;
  var siblingElements = parentElement.children;

  for (var i = 0; i < siblingElements.length; i++) {
    if (siblingElements[i] !== contentElement && siblingElements[i].className === 'content') {
      siblingElements[i].style.display = "none";
      // classForContentIdButton(siblingElements[i].id, "btn btn-secondary");
      classForContentIdButton(siblingElements[i].id, "switcher-button");
    }
  }
}

function showContentAndParents(contentId) {
  // Display the content
  var content = document.getElementById(contentId);
  content.style.display = "block";
  classForContentIdButton(contentId, "switcher-button switcher-button-active");

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

function classForContentIdButton(contentId, klass) {
  var button = document.getElementById(contentId.replace("page_", "btn_"));
  button.className = klass;
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

