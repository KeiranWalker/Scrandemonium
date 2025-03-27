$(document).ready(function() {
    $('[id="highlight"]').hover(
        function() {
            $(this).data('original-bg', $(this).css('background-color'));
            $(this).css('background-color', '#ffe35c');
        },
        function() {
            $(this).css('background-color', $(this).data('original-bg'));
        }
    );

    $('#recipe-btn').click(function() {
        alert('You have added a recipe!');
    }
    );

    var isFavourited = false;

    $(document).on('click', '#favourite-btn', function() {
        if (isFavourited) {
            alert('You have removed this recipe from favourites!');
            isFavourited = false;
        } else {
            alert('You have favourited this recipe!');
            isFavourited = true;
        }
    });
        
});