import axios from "axios";
import ora from "ora";
import { table } from "table";
import chalk from "chalk";
import { PipelineConfig } from "../utils/config.js";
import { logger } from "../utils/logger.js";

interface DagRun {
  dag_run_id: string;
  state: "success" | "failed" | "running" | "queued";
  start_date: string;
  end_date: string;
  duration?: number;
}

function stateColor(state: string): string {
  switch (state) {
    case "success": return chalk.green(state);
    case "failed":  return chalk.red(state);
    case "running": return chalk.cyan(state);
    default:        return chalk.yellow(state);
  }
}

export async function inspectCommand(
  dagId: string,
  config: PipelineConfig
): Promise<void> {
  logger.header(`Inspecting DAG: ${dagId}`);

  const spinner = ora("Connecting to Airflow...").start();
  const auth = { username: config.airflowUser, password: config.airflowPass };
  const base = config.airflowUrl.replace(/\/$/, "");

  try {
    // DAG details
    const dagRes = await axios.get(`${base}/api/v1/dags/${dagId}`, { auth });
    const dag = dagRes.data;
    spinner.succeed("Connected");

    logger.info(`Schedule:   ${dag.schedule_interval?.value ?? "manual"}`);
    logger.info(`Is paused:  ${dag.is_paused ? chalk.yellow("yes") : chalk.green("no")}`);
    logger.info(`File:       ${dag.fileloc}`);

    // Recent runs
    const runsRes = await axios.get(
      `${base}/api/v1/dags/${dagId}/dagRuns?limit=5&order_by=-start_date`,
      { auth }
    );
    const runs: DagRun[] = runsRes.data.dag_runs;

    if (runs.length === 0) {
      logger.warn("No DAG runs found.");
      return;
    }

    logger.header("Recent runs");
    const rows = runs.map((r) => [
      r.dag_run_id.slice(-20),
      stateColor(r.state),
      r.start_date ? new Date(r.start_date).toLocaleString() : "—",
      r.end_date   ? `${Math.round((new Date(r.end_date).getTime() - new Date(r.start_date).getTime()) / 1000)}s` : "—",
    ]);

    console.log(
      table(
        [["Run ID", "State", "Started", "Duration"], ...rows],
        { columns: [{ width: 22 }, { width: 10 }, { width: 24 }, { width: 10 }] }
      )
    );
  } catch (err: any) {
    spinner.fail("Failed to connect");
    if (err.response?.status === 401) {
      logger.error("Auth failed — check AIRFLOW_USER and AIRFLOW_PASS in .env");
    } else if (err.response?.status === 404) {
      logger.error(`DAG '${dagId}' not found. Is it deployed?`);
    } else {
      logger.error(err.message);
    }
    process.exit(1);
  }
}
