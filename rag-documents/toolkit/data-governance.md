> This content is from the AI Toolkit resource: Why Enterprise AI Data Governance Gets It Wrong, part of the AI Skills Passport for SoMM staff at Curtin University.

# Why Enterprise AI Data Governance Gets It Wrong

## Introduction

Organisations across every sector are grappling with data governance policies for AI tools. Many have landed on blanket prohibitions: "do not upload company documents to AI." These policies treat all AI interaction as equally risky. They often conflate several distinct concerns, some legitimate and some based on fundamental misunderstandings of how large language models work. Untangling these concerns is essential for making informed, proportionate decisions about AI adoption.

## The Legitimate Concerns

The rational core of enterprise caution is usually about the **pipeline before training**: the transmission, processing, and storage of data, not about what happens inside the model itself.

### Data Residency and Sovereignty

Many regulations (GDPR, the Australian Privacy Act, sector-specific frameworks) require certain categories of data to remain within specific jurisdictions or within controlled systems. When an employee pastes a document into a consumer AI tool, that text is transmitted to and processed on external infrastructure, often in a different country. This may constitute a compliance violation regardless of what the AI provider does with the data afterwards. The act of transmission itself is the issue.

### Contractual Obligations

NDAs, client agreements, and government contracts frequently define exactly which systems may process covered data. Sending that data to a third-party AI service may breach those terms even if the provider handles it perfectly. The question isn't whether the AI is trustworthy. It's whether the contract permits it.

### Logging and Retention

AI providers may retain prompts and conversations for safety monitoring, abuse detection, or debugging purposes. This is distinct from training. But it still means a sensitive document is sitting on someone else's servers for some retention period. Enterprise agreements typically negotiate specific terms around logging and retention, which is a key reason these agreements exist and why the distinction between consumer and enterprise tiers matters.

### Supply Chain Risk

AI providers, like any SaaS vendor, can be breached. This isn't the model leaking data through its outputs. It's the company's servers being compromised and conversation logs being exfiltrated. This is a standard information security concern that applies to any external service, and it's managed through vendor risk assessments, data processing agreements, and enterprise-tier controls.

## Where the Reasoning Goes Wrong

The problems emerge when organisations conflate these legitimate infrastructure and legal concerns with fears about model behaviour, specifically, the belief that someone could extract uploaded documents from the model itself.

This fear misunderstands how LLMs work at a fundamental level. LLMs interpolate; they do not retrieve. If data is used for training at all (enterprise tiers typically exclude it), it becomes a vanishingly small statistical signal distributed across billions of parameters. It is not stored as a retrievable file. It is not sitting in a searchable database. It is dissolved into the model's general capability like a drop of ink in a swimming pool. There is no mechanism by which another user could query the model and reconstruct your document, because the model never stored it as a document in the first place.

When policies don't make this distinction, the result is blanket prohibition rather than proportionate risk management.

## The Double Standard

The irony is that many organisations enforcing strict AI prohibitions happily allow employees to paste sensitive content into email, cloud storage, Slack, shared drives, and dozens of other SaaS tools, all of which carry the exact same transmission, storage, and jurisdictional considerations. Some of these tools present arguably greater risks: an email can be forwarded to anyone, a shared document can be accessed by anyone with the link, and a Slack message persists in searchable plaintext.

AI feels riskier because it is newer and less understood, not because the actual risk profile is meaningfully different from other cloud services. The governance framework should be consistent: if an organisation has a data classification scheme and a set of approved tools for each classification level, AI tools should simply be evaluated against the same criteria.

## A More Useful Framework

Rather than "don't upload anything to AI," a proportionate policy would address the actual risks:

1. **Classify the data**: What category does this information fall into? Public, internal, confidential, regulated?
2. **Match the tool to the classification**: Enterprise AI tools with data processing agreements are appropriate for internal and some confidential data. Consumer tools are appropriate for public and non-sensitive internal work. Regulated data needs specific assessment against the relevant legislation.
3. **Manage the real risks**: Never paste credentials, API keys, or access tokens. De-identify personal information. Understand the provider's logging and retention terms.
4. **Drop the fictional risks**: Stop treating model extraction as a plausible threat. Stop conflating jailbreaking with data access. Focus governance effort where the actual exposure exists: transmission, storage, jurisdiction, and contractual compliance.

The goal is professional data hygiene applied consistently across all tools, not AI exceptionalism driven by misunderstanding.
