const { chromium } = require("playwright");
const fs = require("fs");
const path = require("path");

const baseUrl = process.env.DEMO_BASE_URL || "http://127.0.0.1:5000";
const videoDir = path.resolve(__dirname, "..", "output", "video", "raw");
fs.mkdirSync(videoDir, { recursive: true });

const wait = (page, seconds) => page.waitForTimeout(seconds * 1000);

async function setCaption(page, title, body) {
  await page.evaluate(
    ({ title, body }) => {
      let box = document.querySelector("#demo-caption");
      if (!box) {
        box = document.createElement("div");
        box.id = "demo-caption";
        Object.assign(box.style, {
          position: "fixed",
          left: "24px",
          right: "24px",
          bottom: "24px",
          zIndex: "9999",
          background: "rgba(17, 24, 39, 0.92)",
          color: "white",
          borderRadius: "8px",
          padding: "16px 18px",
          fontFamily: "Arial, sans-serif",
          boxShadow: "0 14px 36px rgba(0,0,0,0.28)",
          maxWidth: "860px",
          pointerEvents: "none",
        });
        document.body.appendChild(box);
      }
      box.innerHTML = `
        <div style="font-size: 20px; font-weight: 700; margin-bottom: 6px;">${title}</div>
        <div style="font-size: 16px; line-height: 1.45;">${body}</div>
      `;
    },
    { title, body }
  );
}

async function main() {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width: 1280, height: 720 },
    recordVideo: { dir: videoDir, size: { width: 1280, height: 720 } },
  });
  const page = await context.newPage();

  await page.goto(baseUrl);
  await setCaption(
    page,
    "UniHelp Planner - Challenge 3 Student Help",
    "Product vision: help university students manage academic workload, find suitable support resources, and reflect on wellbeing in one focused platform."
  );
  await wait(page, 18);

  await page.getByRole("link", { name: "Workload", exact: true }).click();
  await setCaption(
    page,
    "Story S1 - Academic workload planner",
    "Acceptance criteria: given a student enters a task, deadline, estimated hours, and difficulty, the system saves the task and shows a prioritised list with advice."
  );
  await wait(page, 12);
  await page.getByRole("textbox", { name: "Task title" }).fill("Database coursework draft");
  await wait(page, 4);
  await page.getByRole("textbox", { name: "Module" }).fill("Building Useable Software");
  await wait(page, 4);
  await page.getByRole("textbox", { name: "Deadline" }).fill("2026-05-04");
  await wait(page, 4);
  await page.getByRole("spinbutton", { name: "Estimated hours" }).fill("8");
  await wait(page, 4);
  await page.getByRole("combobox", { name: "Difficulty" }).selectOption("5");
  await wait(page, 4);
  await page.getByRole("button", { name: "Add and prioritise" }).click();
  await setCaption(
    page,
    "S1 result - input, processing, output",
    "The app processes deadline, workload, and difficulty into a priority score. The visible output tells the student what to start first."
  );
  await wait(page, 18);

  await page.getByRole("link", { name: "Support Finder", exact: true }).click();
  await setCaption(
    page,
    "Story S2 - Support resource finder",
    "Acceptance criteria: given a student selects a problem category and urgency, the system returns matching support resources and contact routes."
  );
  await wait(page, 12);
  await page.getByRole("combobox", { name: "What do you need help with?" }).selectOption("wellbeing");
  await wait(page, 5);
  await page.getByRole("combobox", { name: "Urgency" }).selectOption("urgent");
  await wait(page, 5);
  await page.getByRole("button", { name: "Show resources" }).click();
  await setCaption(
    page,
    "S2 result - relevant support routes",
    "The app shows wellbeing resources and urgent support. This reduces the problem of fragmented university support information."
  );
  await wait(page, 20);

  await page.getByRole("link", { name: "Wellbeing", exact: true }).click();
  await setCaption(
    page,
    "Story S3 - Wellbeing check-in",
    "Acceptance criteria: given mood, stress, and sleep values, the system stores the check-in and shows a risk-level recommendation."
  );
  await wait(page, 12);
  await page.getByLabel("Mood today").fill("2");
  await wait(page, 4);
  await page.getByLabel("Stress level").fill("9");
  await wait(page, 4);
  await page.getByRole("spinbutton", { name: "Sleep last night" }).fill("4");
  await wait(page, 4);
  await page.getByRole("textbox", { name: "Notes" }).fill("Feeling overloaded before several deadlines.");
  await wait(page, 5);
  await page.getByRole("button", { name: "Save check-in" }).click();
  await setCaption(
    page,
    "S3 result - wellbeing recommendation",
    "High stress and low mood produce a high-pressure recommendation. The result connects the student to wellbeing support and an academic tutor."
  );
  await wait(page, 22);

  await page.goto(baseUrl);
  await setCaption(
    page,
    "Prototype summary",
    "This MVP demonstrates three complete user stories: workload planning, support resource discovery, and wellbeing guidance. Each flow shows input, processing, output, and acceptance criteria evidence."
  );
  await wait(page, 22);

  const video = await page.video().path();
  await context.close();
  await browser.close();

  const finalRaw = path.resolve(__dirname, "..", "output", "video", "unihelp_demo_raw.webm");
  fs.copyFileSync(video, finalRaw);
  console.log(finalRaw);
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
