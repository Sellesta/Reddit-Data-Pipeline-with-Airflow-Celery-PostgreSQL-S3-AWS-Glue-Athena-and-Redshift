import * as dotenv from "dotenv";
dotenv.config();

export interface PipelineConfig {
  airflowUrl: string;
  airflowUser: string;
  airflowPass: string;
  s3Bucket: string;
  redshiftHost: string;
  redditClientId: string;
  subreddit: string;
  postLimit: number;
}

export function loadConfig(): PipelineConfig {
  return {
    airflowUrl:    process.env.AIRFLOW_URL      || "http://localhost:8080",
    airflowUser:   process.env.AIRFLOW_USER     || "airflow",
    airflowPass:   process.env.AIRFLOW_PASS     || "airflow",
    s3Bucket:      process.env.S3_BUCKET        || "",
    redshiftHost:  process.env.REDSHIFT_HOST    || "",
    redditClientId:process.env.REDDIT_CLIENT_ID || "",
    subreddit:     process.env.TARGET_SUBREDDIT || "dataengineering",
    postLimit:     parseInt(process.env.POST_LIMIT || "100"),
  };
}

export function validateConfig(config: PipelineConfig): string[] {
  const missing: string[] = [];
  if (!config.s3Bucket)       missing.push("S3_BUCKET");
  if (!config.redshiftHost)   missing.push("REDSHIFT_HOST");
  if (!config.redditClientId) missing.push("REDDIT_CLIENT_ID");
  return missing;
}
