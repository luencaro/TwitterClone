(function () {
  function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) {
      return parts.pop().split(';').shift();
    }
    return null;
  }

  function updateLikeState(form, data) {
    const button = form.querySelector('.like-button');
    if (!button) {
      return;
    }
    button.classList.toggle('liked', Boolean(data.liked));
    button.setAttribute('aria-pressed', data.liked ? 'true' : 'false');

    const postId = form.dataset.postId;
    if (postId) {
      const counter = document.querySelector(`[data-like-count="${postId}"]`);
      if (counter) {
        counter.textContent = data.likes;
      }
    }
  }

  document.addEventListener('DOMContentLoaded', function () {
    const likeForms = document.querySelectorAll('.js-like-form');
    if (!likeForms.length) {
      return;
    }

    const csrftoken = getCookie('csrftoken');

    likeForms.forEach(function (form) {
      form.addEventListener('submit', async function (event) {
        event.preventDefault();

        if (!csrftoken) {
          form.submit();
          return;
        }

        try {
          const response = await fetch(form.action, {
            method: 'POST',
            headers: {
              'X-CSRFToken': csrftoken,
              'X-Requested-With': 'XMLHttpRequest',
              'Accept': 'application/json'
            },
            credentials: 'same-origin'
          });

          if (response.status === 401 || response.status === 403) {
            const redirectUrl = form.dataset.loginUrl;
            if (redirectUrl) {
              window.location.href = redirectUrl;
              return;
            }
          }

          if (!response.ok) {
            throw new Error('Like request failed');
          }

          const data = await response.json();
          updateLikeState(form, data);
        } catch (error) {
          form.submit();
        }
      });
    });
  });
})();
