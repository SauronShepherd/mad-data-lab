# MDL-8 submission runbook

This is the final human/external handoff for the already validated engineering release. CI is intentionally excluded by owner instruction.

## 1. Review the frozen package

Use the newest `release-report/MDL-8/mad-data-lab-submission-package-v15.zip`. It contains the current `submission-manifest.json`; verify that the archive contains the narrated demo, screenshots, UI diagnostic, Databricks deployment evidence and final acceptance matrix.

## 2. Review the demo

Open `release-report/MDL-8/MDL-8-demo-narrated.mp4` at normal playback. Accept only if the voice, timing, cursor absence/placement and music level are suitable for publication. The machine checks already confirm 164 seconds, 1920×1080, H.264/AAC and the required narrative content.

## 3. Artwork gate

Human artwork approval is excluded by owner instruction. Use the existing asset/image preflight evidence and do not invent approval records.

## 4. Confirm public links

The deployed URL is `https://mad-data-lab-7474643947913626.aws.databricksapps.com` (redeployed 2026-08-30 under a new Databricks Free Edition account after the prior account exhausted credits; the earlier `...7474654810500477...` URL is dead). It has passed authenticated smoke/soak and public-route HTTP checks against this account. The app requires a Databricks-authenticated session (`CAN_USE` permission) to load — grant reviewer access if the challenge requires unauthenticated viewing, or rely on the narrated demo video as the primary proof of a working app. Paste the final accepted public URL(s) into the article and submission form, then rerun the link checks.

## 5. Submit

Attach the ZIP, narrated MP4, article and required screenshots. Use the challenge framing in the archived Community Article. Record the submission ID/date in the final release report.

## Exit criteria

Promote the release state to `READY_TO_SUBMIT` after the package/link/form steps are complete. The repository's technical state is `ENGINEERING_COMPLETE_SUBMISSION_FORM_PENDING` until the external form is submitted.
