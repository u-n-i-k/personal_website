<template>
  <div :id="block_id">
    <h2>
      {{ $t("common.contacts.title") }}
      <a class="headerlink" :href="'#' + block_id">#</a>
    </h2>
    <div class="contacts row">
      <div class="socials">
        <p>Telegram: <a href="https://t.me/u_n_1_k" target="_blank" rel="noopener noreferrer">@u_n_1_k</a></p>
        <p>LinkedIn: <a href="https://www.linkedin.com/in/u-n-i-k/" target="_blank" rel="noopener noreferrer">u-n-i-k</a></p>
        <p>{{ $t("common.contacts.email") }}: <a href="mailto:u-n-1-k@ya.ru" target="_blank" rel="noopener noreferrer">u-n-1-k@ya.ru</a></p>
      </div>
      <form class="contacts-form" ref="contacts_form" :class="!recaptcha_widget_id === null ? 'hidden': ''" @submit.prevent="preventSubmit">
        <div class="row gap large">
          <div class="group small">
            <input type="name" v-model="name">
            <label :class="name ? 'hidden': ''">{{ $t('common.contacts.name') }}</label>
          </div>
          <div class="group small">
            <input type="email" v-model="email" required minlength=3>
            <label :class="email ? 'hidden': ''">{{ $t('common.contacts.email') }}</label>
          </div>
        </div>
        <div class="group large">
          <textarea v-model="message" ref="message" required minlength=10></textarea>
          <label :class="message ? 'hidden': ''">{{ $t('common.contacts.message') }}</label>
        </div>
        <div class="row gap large">
          <p class="recaptcha-branding">
            This site is protected by reCAPTCHA and the Google
            <a target="_blank" rel="noopener noreferrer" href="https://policies.google.com/privacy">Privacy Policy</a> and
            <a target="_blank" rel="noopener noreferrer" href="https://policies.google.com/terms">Terms of Service</a> apply.
          </p>
          <div :id="block_id + '_grecaptcha'"></div>
          <input type="submit" v-model="button_text" :class="state">
        </div>
      </form>
    </div>
  </div>
</template>
  
<style scoped>
  h2 {
    padding-top: var(--indent);
    border-bottom: 2px solid var(--color-background-2);
  }

  .recaptcha-branding {
    font-size: .7rem;
    padding: 0;
    margin: 0;
    margin-block-start: 0;
    margin-block-end: 0;
  }

  label {
    font-size: 1rem;
    color: var(--color-text-3);
  }

  .contacts-form {
    /* max-width: 500px; */
    display: flex;
    flex-wrap: wrap;
    flex-direction: row;
    justify-content: space-between;
    gap: var(--indent);
    margin: var(--indent) 0;
  }

  .group {
    position:relative;
  }

  .group > label{
    position: absolute;
    top: .3rem;
    left: .7rem;
    pointer-events: none;
  }

  .group > input {
    width: 100%;
  }

  input {
    display: block;
    padding: .6rem;
    border-radius: .25rem;
  }

  input[type="submit"] {
	  transition: background 0.2s ease-in-out;
  }
  input[type="submit"].sending {background: #a98307;}
  input[type="submit"].sent {background: #35682d;}
  input[type="submit"].error {background: #900020;}

  .large {
    width: 100%;
  }

  input[type="submit"] {
    cursor: pointer;
  }

  button:focus {
    background: var(--color-background-3);
    color: var(--color-text);
  }
  
  .row {
    display: flex;
    flex-wrap: nowrap;
    justify-content: space-between;
  }

  .gap {
    gap: calc(var(--indent));
  }

  @media screen and (min-width: 720px) {
    .row {
      flex-direction: row;
    }
    .small {
      width: calc(50% - var(--indent) / 2);
    }
  }

  @media screen and (max-width: 719px) {
    .row {
      flex-direction: column;
    }
    .small {
      width: 100%;
    }
  }

  .contacts {
    display: flex;
    flex-wrap: nowrap;
    --indent: 1rem;
  }

  .socials {
    min-width: 300px;
  }

  textarea {
    padding: .6rem;
    border-radius: .25rem;
    width: 100%;
    resize: none;
    overflow: hidden
  }

  .socials {
    margin: var(--indent) 0;
  }
</style>

<script lang="ts">
  const state_to_text: {[key: string]: string} = {
    ready_to_send: "common.contacts.submit",
    sending: "common.contacts.sending",
    sent: "common.contacts.sent",
    error: "common.contacts.error"
  }
  export default {
    props: {
      block_id: String,
    },
    data() {
      return {
        api_url: import.meta.env.VITE_API_ROOT + "me/contact",
        sitekey:  import.meta.env.VITE_RECAPTCHA_PUBLIC_SITEKEY,
        state: "",
        name: "",
        email: "",
        message: "",
        token: "",
        recaptcha_widget_id: null,
        button_text: ""
      };
    },
    mounted() {
      this.renderRecaptcha();
      this.resizeMessageTextarea();
      this.state = "ready_to_send";
    },

    watch: {
      name() {
        this.state = "ready_to_send";
      },
      email() {
        this.state = "ready_to_send";
      },
      message() {
        this.resizeMessageTextarea();
        this.state = "ready_to_send";
      },
      state() {
        this.button_text = this.$t(state_to_text[this.state]);
      }
    },

    methods: {
      resizeMessageTextarea() {
        let elem: any = this.$refs["message"]
        elem.style.height = "0px";
        elem.style.height = (elem.scrollHeight)+"px";
      },
      renderRecaptcha() {
        try {
          window.grecaptcha.ready(() => {
            this.recaptcha_widget_id = window.grecaptcha.render(
              this.block_id + "_grecaptcha",
              {
                "sitekey" : this.sitekey,
                "size": "invisible"
              }
            );
          });
        } catch(e) {
          console.log(e)
          setTimeout(() => {this.renderRecaptcha()}, 300);
        }
      },
      async preventSubmit() {
        window.grecaptcha.execute(
          this.recaptcha_widget_id,
          {action: this.block_id}
        )
        var recaptcha_token = null;
        while(!recaptcha_token){
          await new Promise(r => setTimeout(r, 100));
          recaptcha_token = window.grecaptcha.getResponse(this.recaptcha_widget_id);
        }
        this.state = "sending";
        let req_body = {
          email: this.email,
          message: "Name:\n" + this.name + "\n\nMessage:\n" + this.message,
          recaptcha_token: recaptcha_token,
        };
        this.axios.post(this.api_url, req_body).then(
          (response) => {
            this.state = "sent";
            window.grecaptcha.reset();
          }
        ).catch(
          (error) => {
            console.log(error);
            this.state = "error";
          }
        ).finally(
          window.grecaptcha.reset(this.recaptcha_widget_id)
        );
      }
    }
  };
</script>