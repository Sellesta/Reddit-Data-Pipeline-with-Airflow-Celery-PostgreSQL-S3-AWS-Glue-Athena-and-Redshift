#!/usr/bin/env node
import { Command } from "commander";
import chalk from "chalk";
import { loadConfig } from "./utils/config.js";
import { inspectCommand } from "./commands/inspect.js";
import { validateCommand } from "./commands/validate.js";
import { reportCommand } from "./commands/report.js";

const config = loadConfig();

const program = new Command();

program
  .name("retl")
  .description(
    chalk.bold("reddit-etl-cli") +
    " — TypeScript CLI companion for the Reddit data pipeline"
  )
  .version("1.0.0");

program
  .command("inspect <dag-id>")
  .description("Show recent DAG runs and status from Airflow")
  .action((dagId: string) => inspectCommand(dagId, config));

program
  .command("validate")
  .description("Check that all required environment variables are set")
  .action(() => validateCommand(config));

program
  .command("report <dag-id> <run-id>")
  .description("Print a task-level breakdown of a specific DAG run")
  .action((dagId: string, runId: string) => reportCommand(dagId, runId, config));

program.parse(process.argv);
