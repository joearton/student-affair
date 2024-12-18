<script>
    import { preferences } from '../stores/preferences';

    $: email = $preferences[0]?.contact_email;
    $: phone = $preferences[0]?.contact_phone;
    $: social_link = $preferences[0]?.social_medias;
</script>
    

<div class="container px-4">
    <div class="d-flex justify-content-between align-items-center">
        <div class="social-icons">
            <a href={social_link?.facebook_url} target="_blank" class="me-3" aria-label="Facebook URl">
                <i class="fab fa-facebook-f"></i>
            </a>
            <a href={social_link?.twitter_url} target="_blank" class="me-3" aria-label="Twitter URl">
                <i class="fab fa-twitter"></i>
            </a>
            <a href={social_link?.instagram_url} target="_blank" class="me-3" aria-label="Instagram URl">
                <i class="fab fa-instagram"></i> 
            </a>
            <a href={social_link?.linkedin_url} target="_blank" class="me-3" aria-label="LinkedIn URl">
                <i class="fab fa-linkedin-in"></i>
            </a>
            <a href={social_link?.youtube_url} target="_blank" class="me-3" aria-label="Youtube URl">
                <i class="fab fa-youtube"></i>
            </a>
        </div>
    
        <div class="contact-info">
            <a href=mailto:{email} class="me-3">
                <i class="fas fa-envelope"></i> Email
            </a>
            <a href=tel:{phone}>
                <i class="fas fa-phone-alt"></i> Contact
            </a>
        </div>    
    </div>
</div>  
