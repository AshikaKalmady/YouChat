function toggleIframe() {
  let iframe = document.getElementById("streamlitIframe");
  if (!iframe) {
    // Create the iframe
    iframe = document.createElement("iframe");
    iframe.id = "streamlitIframe";
    iframe.style.height = "100%";
    iframe.style.width = "25%";
    iframe.style.position = "fixed";
    iframe.style.right = "0";
    iframe.style.top = "0";
    iframe.style.zIndex = "1000";
    iframe.src = "http://localhost:8501";
    iframe.frameBorder = "0"; // Remove the border for a cleaner look
    document.body.appendChild(iframe);

    // Create and style the close button
    var closeButton = document.createElement("button");
    closeButton.textContent = "×"; // Using a simple 'x' character
    closeButton.style.position = "fixed";
    closeButton.style.top = "10px";
    closeButton.style.right = "26%"; // Positioning it just outside the iframe
    closeButton.style.zIndex = "1001";
    closeButton.style.background = "none";
    closeButton.style.border = "none";
    closeButton.style.color = "#aaa"; // Light grey color
    closeButton.style.fontSize = "24px"; // Larger font size for better visibility
    closeButton.style.cursor = "pointer"; // Cursor indicates clickable
    closeButton.style.opacity = "0.6"; // Semi-transparent

    // Add hover effect
    closeButton.onmouseover = function () {
      closeButton.style.opacity = "1"; // Fully opaque on hover
    };
    closeButton.onmouseout = function () {
      closeButton.style.opacity = "0.6"; // Back to semi-transparent
    };

    // Functionality to close the iframe
    closeButton.onclick = function () {
      iframe.parentNode.removeChild(iframe);
      closeButton.parentNode.removeChild(closeButton);
      document.body.style.marginRight = "0";
    };

    document.body.appendChild(closeButton);
    document.body.style.marginRight = "25%";
  } else {
    // If the iframe is already there, toggle its visibility
    iframe.style.display = iframe.style.display === "none" ? "block" : "none";
    document.body.style.marginRight =
      iframe.style.display === "none" ? "0" : "25%";
  }
}

toggleIframe();
