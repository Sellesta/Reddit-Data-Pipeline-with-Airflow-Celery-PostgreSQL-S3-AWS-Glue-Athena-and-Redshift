import chalk from "chalk";
import { PipelineConfig, validateConfig } from "../utils/config.js";
import { logger } from "../utils/logger.js";

const REQUIRED_ENV = [
  { key: "AIRFLOW_URL",       desc: "Airflow web server URL",       example: "http://localhost:8080" },
  { key: "S3_BUCKET",         desc: "S3 bucket for raw data",       example: "reddit-raw-data-moses" },
  { key: "REDSHIFT_HOST",     desc: "Redshift cluster endpoint",    example: "cluster.abc.us-east-1.redshift.amazonaws.com" },
  { key: "REDDIT_CLIENT_ID",  desc: "Reddit API client ID",         example: "abc123xyz" },
  { key: "TARGET_SUBREDDIT",  desc: "Subreddit to pull from",       example: "dataengineering" },
];

export async function validateCommand(config: PipelineConfig): Promise<void> {
  logger.header("Config validation");

  let allGood = true;
  for (const { key, desc, example } of REQUIRED_ENV) {
    const val = process.env[key];
    if (val) {
      const display = key.includes("SECRET") || key.includes("PASS")
        ? "••••••••"
        : val.length > 40 ? val.slice(0, 40) + "…" : val;
      logger.success(`${key.padEnd(25)} ${chalk.dim(display)}`);
    } else {
      logger.error(`${key.padEnd(25)} ${chalk.dim("not set")}  →  ${chalk.dim("e.g. " + example)}`);
      logger.dim(desc);
      allGood = false;
    }
  }

  console.log();
  const missing = validateConfig(config);
  if (allGood) {
    logger.success("All required variables are set. Ready to run.");
  } else {
    logger.warn(`${missing.length} required variable(s) missing.`);
    logger.dim('Copy airflow.env → .env and fill in the blanks.');
    process.exit(1);
  }
}
