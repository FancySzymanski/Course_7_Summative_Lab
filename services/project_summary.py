def build_summary_prompt(project):
    tasks = "\n".join(
        f"- {t.title} ({t.status}, assigned to {t.assigned_to or 'Unknown'})"
        for t in project.tasks
    ) or "No tasks yet."

    return (
        "Summarize this project for a team lead. Give a short summary, "
        "one risk note, and one suggested next step.\n"
        "Rules: do not invent details; write 'Unknown' where information is missing.\n\n"
        f"Project: {project.title}\n"
        f"Description: {project.description or 'Unknown'}\n"
        f"Due date: {project.due_date or 'Unknown'}\n"
        f"Tasks:\n{tasks}"
    )


def summarize_project(ai_client, project):
    return ai_client.send(build_summary_prompt(project))