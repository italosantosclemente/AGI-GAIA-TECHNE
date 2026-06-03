# Public Gaia-Techne Chat Deploy

GitHub README can expose the Gaia-Techne chat as a visible public doorway, but it cannot execute the Streamlit/Python app by itself. GitHub Pages is useful for static documentation; the live chat needs a Python app host.

Recommended public host:

```text
Streamlit Community Cloud
```

Repository settings for deploy:

```text
Repository: italosantosclemente/AGI-GAIA-TECHNE
Branch: main
Main file path: ui/gaia_llm_chat_app.py
Dependency file: ui/requirements.txt
Suggested app URL: agi-gaia-techne.streamlit.app
```

After deploy, paste the final public URL into the top "Converse Com Gaia-Techne" section of `README.md`.

## What Works Publicly Before A Checkpoint

The public app can run in bootstrap CTK/CHK mode without `models/agt-gaia-manual-gpt/latest.pt`.

Visible chat commands:

```text
fazer telemetria
```

```text
Boa tarde. Hoje e dia 030626. Declaro o primeiro contato direto de um humano com Gaia.
```

`fazer telemetria` collects public source signals at request time and returns a finite judgment on Gaia-human symbiosis. This is the safest first public capability because it does not require storing large model weights in GitHub.

## What Needs A Model Artifact Later

The trained ManualGPT checkpoint should not be committed directly to Git if it grows large. Use one of these paths later:

- Train locally and upload the checkpoint to the hosting environment if the file size is allowed.
- Use Git LFS if the host supports it and the file stays within limits.
- Move the checkpoint to a model host or object store and load it at app startup.

Until then, the app remains honest: bootstrap CTK/CHK, first-contact trace, web context, telemetry and public audit.

## Source Anchors

- Streamlit Community Cloud deploys an app by repository, branch and entrypoint file: https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy
- Streamlit Community Cloud can use a `requirements.txt` in the same directory as the app entrypoint: https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/app-dependencies
- GitHub Pages publishes static files and does not support Python server-side execution: https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site
