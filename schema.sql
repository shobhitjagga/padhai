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
    scheduled_at timestamptz not null,
    sent_at      timestamptz,
    created_at   timestamptz default now()
);
