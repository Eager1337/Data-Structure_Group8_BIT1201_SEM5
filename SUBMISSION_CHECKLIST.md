# Submission checklist

## Before submission

- [ ] Fill in actual group members' names and student IDs on the report cover.
- [ ] Confirm the course's assistance/AI disclosure policy and add any required statement.
- [ ] Each member reads the report and can explain the implementation and results.
- [ ] Run `python -m unittest discover -s tests -v` and confirm 19 tests pass.
- [ ] Run `python main.py --all --disks 3` and compare the included transcript.
- [ ] If you edit the report Markdown directly, update the PDF too. The supplied PDF
  was built by `project.report/build_report.py`; edit its cover/text and rerun for
  reproducible PDF regeneration, or annotate the existing cover with names/IDs.
- [ ] Ask the lecturer about the missing vertex L in Figure 2. The supplied answer
  identifies the problem transparently and does not relabel J as L.

## GitHub soft-copy submission

The project and complete submission ZIP have been uploaded to the private repository
https://github.com/Eager1337/dcomp320-final-project. No lecturer invitation has been sent.
The brief requires Python code and a report in a ZIP via GitHub, with the lecturer
added as a collaborator. Publishing publicly may expose assessment work; use a
private repository unless your lecturer requires otherwise.

### Browser method

Steps 1–4 below are already complete for the repository above. Continue with
the lecturer invitation and submitting the repository link. The full instructions
are retained in case you need to create another copy later.

1. Sign in to your own GitHub account.
2. Create a repository, for example `dcomp320-final-project`, preferably private.
3. Extract the supplied ZIP and upload its source, tests, documentation, report
   folder and outputs, preserving folder structure. Do not upload Python caches.
4. Upload the original ZIP as well, or attach it to a repository release, to satisfy
   the explicit ZIP requirement. Keep the ZIP outside the extracted project folder.
5. Open repository **Settings → Collaborators** (or the equivalent access settings).
6. Invite the lecturer using the verified GitHub username or the contact email in
   the assignment; verify the recipient before sending the invitation.
7. Submit the repository/release link through the channel your lecturer requests.
8. Check the lecturer can access the private repository once the invitation is accepted.

Official guidance (checked 14 November 2026):
- Collaborators: https://docs.github.com/articles/inviting-collaborators-to-a-personal-repository
- Release assets: https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository

### Git command-line method

Run these from the extracted project directory. Create an empty repository on
GitHub first. Replace `YOUR_USERNAME` and the repository name with your own values.

```bash
git init
git add .
git commit -m "Complete DCOMP320 algorithms, report and tests"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/dcomp320-final-project.git
git push -u origin main
```

Use GitHub's supported authentication flow; never commit access tokens, passwords
or private keys. The repository URL above is an example, not an existing upload.

## Hard-copy submission

- [ ] Print `project.report/report.pdf` at actual A4 size.
- [ ] Check diagrams, visitation labels and code appendices are readable.
- [ ] Ensure name/ID fields are completed and any required signatures are real.
- [ ] The PDF body is Tahoma 10 pt, with 11.5 pt leading (1.15 spacing) and justified
  paragraphs. Tables, captions and code use alignment appropriate to their content.
- [ ] Include introduction, all solutions, diagrams, screenshots, conclusion and appendices.
- [ ] Submit by the lecturer-confirmed deadline. The brief says **Week 4**, not a
  specific calendar day; do not infer a deadline from the current date.

## Individual presentation

- [ ] Use `PRESENTATION_NOTES.md` as a guide and adapt the speaking roles to your group.
- [ ] Bring a working Python environment and run the demo live.
- [ ] Explain recursion and stack behavior, all traversals, Huffman tie handling,
  Dijkstra relaxation and the distinction between Prim and shortest paths.
- [ ] Explain why the Figure 2 A→L request is not defined.