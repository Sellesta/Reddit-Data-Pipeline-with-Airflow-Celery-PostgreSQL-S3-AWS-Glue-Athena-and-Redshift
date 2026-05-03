import axios from "axios";
import ora from "ora";
import chalk from "chalk";
import { PipelineConfig } from "../utils/config.js";
import { logger } from "../utils/logger.js";

interface TaskInstance {
  task_id: string;
  state: string;
  duration: number | null;
  start_date: string;
}

export async function reportCommand(
  dagId: string,
  runId: string,
  config: PipelineConfig
): Promise<void> {
  logger.header(`Pipeline run report`);
  logger.dim(`DAG: ${dagId}  |  Run: ${runId}`);

  const spinner = ora("Fetching task instances...").start();
  const auth = { username: config.airflowUser, password: config.airflowPass };
  const base = config.airflowUrl.replace(/\/$/, "");

  try {
    const res = await axios.get(
      `${base}/api/v1/dags/${dagId}/dagRuns/${runId}/taskInstances`,
      { auth }
    );
    spinner.succeed("Fetched");

    const tasks: TaskInstance[] = res.data.task_instances;
    const total = tasks.length;
    const succeeded = tasks.filter((t) => t.state === "success").length;
    const failed    = tasks.filter((t) => t.state === "failed").length;
    const skipped   = tasks.filter((t) => t.state === "skipped").length;

    console.log();
    console.log(`  ${chalk.green(`✓ ${succeeded} succeeded`)}  ${chalk.red(`✗ ${failed} failed`)}  ${chalk.dim(`⊘ ${skipped} skipped`)}  of ${total} tasks`);
    console.log();

    const maxDuration = Math.max(...tasks.map((t) => t.duration ?? 0));

    for (const task of tasks) {
      const dur  = task.duration != null ? `${Math.round(task.duration)}s` : "—";
      const bar  = task.duration
        ? chalk.cyan("█".repeat(Math.round((task.duration / maxDuration) * 20)).padEnd(20))
        : " ".repeat(20);
      const stateIcon =
        task.state === "success" ? chalk.green("✓") :
        task.state === "failed"  ? chalk.red("✗")   :
        task.state === "skipped" ? chalk.dim("⊘")   : chalk.yellow("?");

      console.log(`  ${stateIcon} ${task.task_id.padEnd(30)} ${bar} ${chalk.dim(dur.padStart(6))}`);
    }

    if (failed > 0) {
      console.log();
      logger.warn("Some tasks failed. Run `retl inspect " + dagId + "` for details.");
    }
  } catch (err: any) {
    spinner.fail("Request failed");
    logger.error(err.response?.data?.detail ?? err.message);
    process.exit(1);
  }
}
