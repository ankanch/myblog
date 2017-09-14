<?php
/*
Template Name: myblog_theme
*/
 get_header(); ?>

<div id="primary" class="site-content-fullwidth" style="background:white;">
  <div id="content" role="main" style="background:white;">
<div id="myblog_style_page" style="margin-left:45px;margin-right:45px;">
<link rel='stylesheet'  href='http://akakanch.com/wp-content/themes/nisarg/css/bootstrap4alpha.css' type='text/css' />
<script type='text/javascript' src='http://akakanch.com/wp-content/themes/nisarg/js/jquery-3.2.1.min.js'></script>
<link rel='stylesheet'  href='http://akakanch.com/wp-content/themes/nisarg/css/xstyle.css' type='text/css' />
<div class="container">
<?php /* Start the Loop */ ?>
<?php while(have_posts()) : the_post(); ?>
<?php the_content();?>
<?php endwhile; ?>

</div>
</div>
<iframe id="result"  frameBorder="0" style="overflow:hidden;">
</iframe>
  </div><!-- #content -->
</div><!-- #primary -->
<script>
  function resizeIframe(obj) {
    obj.style.height = obj.contentWindow.document.body.scrollHeight + 'px';
  }
    $(document).ready(function () {
		var iframe = document.getElementById('result'),
        iframedoc = iframe.contentDocument || iframe.contentWindow.document;
        var father  = document.getElementById('myblog_style_page');
        iframedoc.body.innerHTML = iframedoc.body.innerHTML + father.innerHTML ;
        resizeIframe(iframe);
		father.innerHTML = "";

    });
</script>
<?php get_footer(); ?>