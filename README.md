# NEXTORA — Website deployment package

This is a polished, responsive **front-end preview** for the NEXTORA professional social network.

## Deploy the website preview

### Vercel (easy option)
1. Create a free account at https://vercel.com/
2. Install Git and create a GitHub repository, then upload the contents of this folder; or use Vercel's dashboard to import the repository.
3. In Vercel, choose **Add New → Project**, import the repository, and deploy.
4. Framework preset: **Other**. Build command: leave blank. Output directory: `public`.
5. Vercel will assign a temporary `*.vercel.app` address.

The included `vercel.json` also configures the public folder.

## Important: preview vs real social network
This package is a front-end preview. Posts and likes are stored only in the current browser session/page; they are not shared between people. Sign-in and registration are intentionally marked as coming soon. Sample headlines are not a live news feed.

A real public launch still needs:
- connect the FastAPI backend and PostgreSQL database;
- real account registration/login, email verification and password recovery;
- shared posts, comments, likes, follows and user profiles;
- moderation, reporting, admin tools and abuse prevention;
- security review, privacy policy, terms and operational monitoring.

Do not advertise this preview as a fully functioning social network yet.
