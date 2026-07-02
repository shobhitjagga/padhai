-- Run this in Supabase SQL Editor before first use

create table if not exists users (
    chat_id    text primary key,
    name       text,
    language   text default 'en',
    created_at timestamp default now()
);

create table if not exists messages (
    id         uuid default gen_random_uuid() primary key,
    chat_id    text,
    text       text,
    intent     text,
    response   text,
    created_at timestamp default now()
);

create table if not exists ai_calls (
    id               uuid default gen_random_uuid() primary key,
    chat_id          text,
    function         text,
    model            text,
    input            text,
    output           text,
    prompt_tokens    int,
    completion_tokens int,
    created_at       timestamp default now()
);

create table if not exists content_evals (
    id              uuid default gen_random_uuid() primary key,
    chat_id         text,
    subject         text,
    topic           text,
    grade           text,
    sel_dimension   text,
    scores          jsonb,       -- full per-metric {verdict, reason} object
    failed_metrics  text[],      -- array of metric names that failed
    passed          boolean,
    created_at      timestamp default now()
);

create table if not exists feedback_jobs (
    id           bigserial primary key,
    chat_id      text not null,
    language     text not null default 'en',
    topic        text not null default '',
    channel      text not null default 'telegram',  -- 'telegram' | 'whatsapp'
    grade        text not null default '',
    subject      text not null default '',
    q4_due       boolean not null default false,
    q4_index     int not null default 0,
    scheduled_at timestamptz not null,
    sent_at      timestamptz,
    created_at   timestamptz default now()
);

-- Per-class profile: one row per (teacher × grade × subject)
-- Accumulates signal from Q2/Q3/Q4 feedback over time.
create table if not exists class_profiles (
    chat_id      text not null,
    grade        text not null,
    subject      text not null,
    primary key (chat_id, grade, subject),

    session_count         int not null default 0,

    -- Q2: SEL engagement style counts
    verbal_high_count     int not null default 0,   -- students opened up verbally
    verbal_mid_count      int not null default 0,   -- mixed verbal/written
    verbal_low_count      int not null default 0,   -- mostly quiet

    -- Q3: classroom energy counts
    energy_focused_count  int not null default 0,
    energy_high_count     int not null default 0,
    energy_low_count      int not null default 0,

    -- Q4 rotating: stable class descriptors (overwritten each time teacher answers)
    persona       text,   -- shy | mixed | assertive
    home_context  text,   -- difficult | mixed | stable
    gender_gap    text,   -- yes | partial | no
    group_pref    text,   -- high | mixed | low

    -- computed majority tendencies (recalculated after each session)
    verbal_tendency  text,   -- high | medium | low
    energy_tendency  text,   -- focused | high | low

    -- Q5: Was the SEL activity actually run in class?
    sel_run_yes_count      int not null default 0,
    sel_run_partial_count  int not null default 0,
    sel_run_no_count       int not null default 0,

    -- Q6: Did a quiet student participate?
    quiet_yes_count        int not null default 0,
    quiet_no_count         int not null default 0,
    quiet_unsure_count     int not null default 0,

    updated_at   timestamptz default now()
);

-- Run these if the table already exists (safe to re-run — ADD COLUMN IF NOT EXISTS)
alter table class_profiles add column if not exists sel_run_yes_count     int not null default 0;
alter table class_profiles add column if not exists sel_run_partial_count int not null default 0;
alter table class_profiles add column if not exists sel_run_no_count      int not null default 0;
alter table class_profiles add column if not exists quiet_yes_count       int not null default 0;
alter table class_profiles add column if not exists quiet_no_count        int not null default 0;
alter table class_profiles add column if not exists quiet_unsure_count    int not null default 0;

-- Content cache: avoid regenerating identical lesson plans
create table if not exists content_cache (
    cache_key  text primary key,          -- sha256 of (subject+topic+grade+sel_dim+language+class_context)
    response   text not null,
    created_at timestamptz default now()
);
