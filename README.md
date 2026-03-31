# Text-to-Hindi Translator

Automated GitHub pipeline that translates uploaded English text files to Hindi and emails the result to the PR author.

## How It Works

1. A user forks this repo and adds a `.txt` file inside the `uploads/` folder
2. They open a **Pull Request** to the main branch
3. The GitHub Actions pipeline automatically:
   - Detects the new `.txt` file(s)
   - Translates the content from English to Hindi
   - Emails the translated file to the PR author's email
4. The repository owner reviews and approves/merges the PR

## Setup Instructions

### 1. Create a GitHub Repository

```bash
cd text-to-hindi-translator
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/text-to-hindi-translator.git
git push -u origin main
```

### 2. Configure GitHub Secrets

Go to **Settings → Secrets and variables → Actions** and add these secrets:

| Secret          | Description                          | Example                  |
| --------------- | ------------------------------------ | ------------------------ |
| `SMTP_HOST`     | SMTP server hostname                 | `smtp.gmail.com`         |
| `SMTP_PORT`     | SMTP server port (TLS)               | `587`                    |
| `SMTP_USER`     | SMTP login username                  | `you@gmail.com`          |
| `SMTP_PASSWORD` | SMTP login password or app password  | `abcd efgh ijkl mnop`   |
| `SENDER_EMAIL`  | The "From" address in the email      | `you@gmail.com`          |

> **Gmail users:** Use an [App Password](https://myaccount.google.com/apppasswords) instead of your real password. Enable 2-Step Verification first.

### 3. Update CODEOWNERS

Edit `.github/CODEOWNERS` and replace `YOUR_GITHUB_USERNAME` with your actual GitHub username. This ensures all PRs require your approval.

### 4. Enable Branch Protection (Required for approval flow)

Go to **Settings → Branches → Add rule** for `main`:

- ✅ Require a pull request before merging
- ✅ Require approvals (set to 1)
- ✅ Require review from Code Owners

This enforces that only you can approve and merge PRs.

## For Contributors

1. Fork this repository
2. Add your `.txt` file to the `uploads/` folder
3. Open a Pull Request to `main`
4. The pipeline will translate your file and email it to your GitHub public email
5. Wait for the owner to review and merge

> **Important:** Your GitHub profile must have a **public email** set, otherwise the pipeline cannot send you the translated file.

## Project Structure

```
text-to-hindi-translator/
├── .github/
│   ├── CODEOWNERS              # Requires owner approval on PRs
│   └── workflows/
│       └── translate-and-email.yml  # GitHub Actions pipeline
├── scripts/
│   └── translate_and_email.py  # Translation + email logic
├── uploads/                    # Users add .txt files here
│   └── README.md
├── requirements.txt
└── README.md
```
