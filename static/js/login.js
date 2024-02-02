<script>
    document.addEventListener("DOMContentLoaded", function(){
        document.querySelectorAll(".toggle-password").forEach(function(toggle) {
            toggle.addEventListener('click', function() {
                const input = document.querySelector(this.getAttribute("toggle"));
                if (input.type === "password") {
                    input.type = "text";
                    this.innerHTML = '&#128064;';  // Closed eye Unicode character when password is shown
                } else {
                    input.type = "password";
                    this.innerHTML = '&#128065;';  // Eye Unicode character when password is hidden
                }
            });
        })
    });
</script>
