## Why this matters to you

Research is only as valuable as your ability to communicate it. You'll need to write conference abstracts, journal papers, grant applications, and internal reports throughout your time in the lab. Learning the structure and conventions of scientific writing early will make every paper you work on smoother and more efficient.

## The structure of a scientific paper

Nearly every empirical neuroscience paper follows the same format (often called IMRaD):

### Abstract (150-300 words)

A self-contained summary of the entire paper. Write it last. It should contain: one sentence of background/motivation, one sentence stating the gap or question, 1-2 sentences on methods, 2-3 on key results, and one on significance/conclusion. Many readers will only read the abstract, so it must stand alone.

### Introduction (1-3 pages)

Starts broad, narrows to your specific question. The structure is often called a "funnel":

- Paragraph 1: Big-picture context (e.g., "Brain connectivity is altered in psychiatric disorders")

- Middle paragraphs: Previous work — what's known, what's been tried, what gaps remain

- Final paragraph: Your specific aim and hypothesis. "In this study, we used Group ICA and dFNC to investigate..."

Every statement of fact needs a citation. The introduction establishes WHY your study matters.

### Methods

Detailed enough that someone could reproduce your work. Standard subsections for neuroimaging papers:

- **Participants**: Sample size, demographics, inclusion/exclusion criteria, IRB approval

- **Data acquisition**: Scanner type, field strength, sequence parameters (TR, TE, flip angle, voxel size, number of volumes)

- **Preprocessing**: Every step with software version and parameters (e.g., "Data were preprocessed using SPM12. Steps included: realignment, coregistration to T1, normalization to MNI space using the unified segmentation approach, and smoothing with a 6mm FWHM Gaussian kernel.")

- **Analysis**: ICA parameters (number of components, algorithm, back-reconstruction method, software version), statistical tests, correction methods

### Results

Report what you found, not what it means (save that for Discussion). Present results in order of your research questions. Include:

- Statistical values: t(98) = 3.45, p = 0.001, d = 0.69

- Figures: Brain maps, FNC matrices, group comparison plots

- Tables: Demographics, component lists, statistical summaries

### Discussion (2-4 pages)

Interpret your findings in context of existing literature:

- Paragraph 1: Summarize main findings (briefly — don't repeat Results)

- Subsequent paragraphs: Compare to previous studies, explain mechanisms, discuss implications

- Limitations paragraph: Be honest about sample size, methodology constraints, generalizability

- Final paragraph: Conclusion and future directions

### References

Use a citation manager. The lab uses APA-style or journal-specific formatting.

## Writing workflow

1. **Outline first**: Create section headings and bullet points before writing prose

2. **Methods first**: Easiest to write because it's factual — what you did

3. **Results second**: Present your findings clearly

4. **Introduction third**: Now you know what you need to set up

5. **Discussion fourth**: Interpret in context

6. **Abstract last**: Summarize everything

## Citation management

Install a citation manager immediately — you'll reference hundreds of papers:

- **[Zotero](https://www.zotero.org/)** (recommended): Free, open-source, syncs across devices, browser extension for one-click saving, Word/Google Docs integration. The lab tends to use Zotero.

- **[Mendeley](https://www.mendeley.com/)**: Free, owned by Elsevier, good PDF annotation, built-in social network for finding papers.

- **[Paperpile](https://paperpile.com/)**: Google Docs integration, clean interface, paid subscription.

All of these:

- Store PDFs and metadata

- Generate formatted bibliographies automatically

- Insert citations while writing with keyboard shortcuts

- Support thousands of journal citation styles

## Authorship norms in academia

Authorship in scientific papers follows conventions that may be unfamiliar:

- **First author**: Did the most work (ran experiments, wrote the paper). As a student/postdoc, this is your goal.

- **Last author**: The senior researcher/PI who supervised the work and provided resources. Typically the lab director.

- **Middle authors**: Contributed intellectually, provided data, helped with analysis, or revised the manuscript.

- **Corresponding author**: Handles communication with the journal. Usually the first or last author.

Discuss authorship expectations with your PI early in any project. The [ICMJE guidelines](http://www.icmje.org/recommendations/browse/roles-and-responsibilities/defining-the-role-of-authors-and-contributors.html) define what qualifies as authorship.

## Common writing mistakes in neuroimaging papers

- Reporting p-values without effect sizes

- Not specifying software versions

- Omitting preprocessing details (voxel size, smoothing kernel, motion criteria)

- Using "significant" for non-statistical differences

- Over-interpreting reverse inference ("this region activated, therefore the subject was experiencing emotion X")

- Not reporting how many subjects were excluded and why

## COBIDAS reporting checklist

The [COBIDAS guidelines](https://doi.org/10.1038/nn.4500) (Committee on Best Practices in Data Analysis and Sharing) define the MINIMUM information that neuroimaging papers must report. Before submitting any paper, verify you've included:

- Scanner manufacturer, model, field strength, coil type

- Sequence parameters: TR, TE, flip angle, voxel size, number of slices, number of volumes, multiband factor

- Every preprocessing step with software version and parameters

- Motion handling: criteria for exclusion, regressors used, scrubbing thresholds

- ICA specifics: number of components, algorithm, back-reconstruction method, GIFT version, component selection criteria

- Statistical tests with degrees of freedom, correction methods, exact thresholds

- Effect sizes (Cohen's d, partial η²) for all reported results

- Number of subjects excluded with specific reasons

- Sample size justification (power analysis if performed)

Missing any of these will draw reviewer criticism and delay publication.

## Resources for deeper learning

- 📺 [How to Write a Research Paper — Prof. Pete Carr](https://www.youtube.com/watch?v=UY7sVKJPTMA)

- 📺 [How to Read a Scientific Paper effectively](https://www.youtube.com/watch?v=jO6wV4QL0dU)

- 📑 [Ten Simple Rules for Writing Research Papers (PLOS Comp Bio)](https://doi.org/10.1371/journal.pcbi.1003453)

- 📄 [Zotero Quick Start Guide](https://www.zotero.org/support/quick_start_guide)

- 📄 [ICMJE Authorship Guidelines](http://www.icmje.org/recommendations/browse/roles-and-responsibilities/defining-the-role-of-authors-and-contributors.html)

- 📄 [COBIDAS guidelines for neuroimaging methods reporting](https://doi.org/10.1038/nn.4500)
