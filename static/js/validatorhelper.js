(function($) {
    $(document).ready(function($) {
        //enable and disable behaviour for Y-right Axis in admin
        enable_cb();
        $("#id_is_y_axis_right_available").click(enable_cb);
    });
    
    function enable_cb() {
         if (this.checked) {
 			$("#id_y_axis_right_labels_labels").removeAttr("disabled");
            $("#id_y_axis_right_labels_colour").removeAttr("disabled");
            $("#id_y_axis_right_colour").removeAttr("disabled");
            $("#id_y_axis_right_grid_colour").removeAttr("disabled");
            $("#id_y_axis_right_offset").removeAttr("disabled");
            $("#id_y_axis_right_stroke").removeAttr("disabled");
            $("#id_y_axis_right_tick_length").removeAttr("disabled");
            $("#id_y_axis_right_min").removeAttr("disabled");
            $("#id_y_axis_right_max").removeAttr("disabled");
            $("#id_y_axis_right_steps").removeAttr("disabled");
         } else {
            $("#id_y_axis_right_labels_labels").attr("disabled", true);
            $("#id_y_axis_right_labels_colour").attr("disabled", true);
            $("#id_y_axis_right_colour").attr("disabled",true);
            $("#id_y_axis_right_grid_colour").attr("disabled",true);
            $("#id_y_axis_right_offset").attr("disabled",true);
            $("#id_y_axis_right_stroke").attr("disabled",true);
            $("#id_y_axis_right_tick_length").attr("disabled",true);
            $("#id_y_axis_right_min").attr("disabled",true);
            $("#id_y_axis_right_max").attr("disabled",true);
            $("#id_y_axis_right_steps").attr("disabled",true);
    }



}
})(django.jQuery);


