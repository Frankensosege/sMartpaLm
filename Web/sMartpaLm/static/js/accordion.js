document.querySelectorAll('.accordion-header').forEach(function(header, index) {
    header.addEventListener('click', function() {
        var isOpen = header.getAttribute('aria-expanded');
        var content = header.nextElementSibling.querySelector('.accordion-body');

        // Check if the accordion is unfolded
        if (isOpen === 'true') {
            // Access the desired variable when the accordion is unfolded
//            var variable = content.getAttribute('admin_list');
//            console.log(variable);
            console.log("Header order: " + index);
        }
    });
});