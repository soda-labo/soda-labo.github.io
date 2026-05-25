import fs from "node:fs";
import path from "node:path";
import yaml from "js-yaml";

const DATA_DIR = path.resolve(process.cwd(), "src/data");

export type Faculty = {
  name: string;
  role: string;
  photo?: string;
  email?: string;
  website?: string;
  scholar?: string;
  cv?: string;
  education?: string[];
};

export type Member = {
  name: string;
  photo?: string;
  website?: string;
  affiliation?: string;
};

export type Alumni = {
  name: string;
  now?: string;
  year?: string;
  website?: string;
};

export type Members = {
  faculty: Faculty[];
  phd_students: Member[];
  visitors: Member[];
  alumni: {
    postdocs: Alumni[];
    graduate_smu: Alumni[];
    undergraduate_smu: Alumni[];
    visitors: Alumni[];
  };
};

export function loadMembers(): Members {
  const raw = fs.readFileSync(path.join(DATA_DIR, "members.yml"), "utf8");
  return yaml.load(raw) as Members;
}
