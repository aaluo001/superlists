
window.superlists = {};
window.superlists.initialize = function() {
    $('input[name="text"]').on('keypress', function() {
        $(".has-error").hide();
    });
};

