"use client";

import { createContext, useContext, useMemo, type ComponentProps } from "react";
import {
  ArrowUpIcon,
  BotIcon,
  CheckIcon,
  ChevronLeftIcon,
  ChevronRightIcon,
  CopyIcon,
  DownloadIcon,
  LoaderIcon,
  PencilIcon,
  RefreshCwIcon,
  SquareIcon,
  ThumbsDownIcon,
  ThumbsUpIcon,
  UserIcon,
} from "lucide-react";
import {
  ActionBarPrimitive,
  AuiIf,
  BranchPickerPrimitive,
  ComposerPrimitive,
  ErrorPrimitive,
  MessagePrimitive,
  ThreadPrimitive,
  useAuiState,
} from "@assistant-ui/react";

import { Button } from "@/components/ui/button";
import { TooltipIconButton } from "@/components/tooltip-icon-button";
import { MarkdownText } from "@/components/markdown-text";
import { ToolFallback } from "@/components/tool-fallback.aui";
import {
  ComposerAddAttachment,
  ComposerAttachments,
  UserMessageAttachments,
} from "@/components/attachment.aui";
import { cn } from "@/lib/utils";
import {
  evidenceUrl,
  parseQueryGraph,
  resolveCitation,
} from "@/lib/query-graph";
const LinearHistory = createContext(false);
const ViewGraph = createContext<
  | ((threadId: string, messageId: string, evidenceId?: string) => void)
  | undefined
>(undefined);

export function Thread({
  linearHistory = false,
  onViewGraph,
}: {
  linearHistory?: boolean;
  onViewGraph?: (
    threadId: string,
    messageId: string,
    evidenceId?: string,
  ) => void;
}) {
  const isEmpty = useAuiState((s) => s.thread.isEmpty);

  return (
    <LinearHistory.Provider value={linearHistory}>
      <ViewGraph.Provider value={onViewGraph}>
        <ThreadPrimitive.Root
          className="bg-background text-foreground flex h-full flex-col text-sm"
          style={{
            ["--background" as string]: "var(--aui-background)",
            ["--foreground" as string]: "var(--aui-foreground)",
            ["--muted-foreground" as string]: "var(--aui-muted-foreground)",
            ["--border" as string]: "var(--aui-border)",
            ["--thread-max-width" as string]: "48rem",
            ["--composer-radius" as string]: "1.5rem",
            ["--composer-padding" as string]: "8px",
            ["--composer-bg" as string]: "var(--aui-composer)",
            ["--accent-color" as string]: "var(--aui-accent)",
            ["--accent-foreground" as string]: "var(--aui-accent-foreground)",
          }}
        >
          <ThreadPrimitive.Viewport
            turnAnchor="top"
            className="relative flex flex-1 flex-col overflow-x-auto overflow-y-scroll scroll-smooth"
          >
            <div
              className={cn(
                "mx-auto flex w-full max-w-[var(--thread-max-width)] flex-1 flex-col px-4 pt-4",
                isEmpty && "justify-center",
              )}
            >
              <AuiIf condition={(s) => s.thread.isEmpty}>
                <ThreadWelcome />
              </AuiIf>

              <div className="mb-14 flex flex-col gap-y-6 empty:hidden">
                <ThreadPrimitive.Messages
                  components={{
                    UserMessage,
                    EditComposer,
                    AssistantMessage,
                  }}
                />
              </div>

              <ThreadPrimitive.ViewportFooter
                className={cn(
                  "bg-background flex w-full flex-col gap-4 overflow-visible pb-4",
                  !isEmpty &&
                    "sticky bottom-0 mt-auto rounded-t-[var(--composer-radius)]",
                )}
              >
                <Composer />
              </ThreadPrimitive.ViewportFooter>
            </div>
          </ThreadPrimitive.Viewport>
        </ThreadPrimitive.Root>
      </ViewGraph.Provider>
    </LinearHistory.Provider>
  );
}
function ThreadWelcome() {
  return (
    <div className="mb-6 flex flex-col px-2">
      <p className="fade-in slide-in-from-bottom-1 animate-in fill-mode-both text-2xl font-medium tracking-tight duration-200">
        How can I help you today?
      </p>
    </div>
  );
}

function Composer() {
  return (
    <ComposerPrimitive.Root className="relative flex w-full flex-col">
      <ComposerPrimitive.AttachmentDropzone
        render={
          <div className="flex w-full cursor-text flex-col gap-2 rounded-[var(--composer-radius)] border border-[color-mix(in_oklab,var(--aui-border)_60%,transparent)] bg-[var(--composer-bg)] p-[var(--composer-padding)] transition-[border-color] focus-within:border-(--aui-border) data-[dragging=true]:border-dashed" />
        }
      >
        <ComposerAttachments />
        <ComposerPrimitive.Input
          placeholder="Send a message..."
          className="placeholder:text-muted-foreground max-h-48 min-h-10 w-full resize-none bg-transparent px-2.5 py-1 text-base leading-6 outline-none"
          rows={1}
          autoFocus
          enterKeyHint="send"
          aria-label="Message input"
        />
        <ComposerAction />
      </ComposerPrimitive.AttachmentDropzone>
    </ComposerPrimitive.Root>
  );
}

function ComposerAction() {
  const linearHistory = useContext(LinearHistory);
  return (
    <div className="relative flex items-center justify-between">
      {!linearHistory && <ComposerAddAttachment />}

      <AuiIf condition={(s) => !s.thread.isRunning}>
        <ComposerPrimitive.Send
          render={
            <TooltipIconButton
              tooltip="Send message"
              side="bottom"
              type="submit"
              variant="default"
              size="icon"
              className="ml-auto size-7 rounded-full"
              style={{
                backgroundColor: "var(--accent-color)",
                color: "var(--accent-foreground)",
              }}
              aria-label="Send message"
            />
          }
        >
          <ArrowUpIcon className="size-4" />
        </ComposerPrimitive.Send>
      </AuiIf>

      <AuiIf condition={(s) => s.thread.isRunning}>
        <ComposerPrimitive.Cancel
          render={
            <Button
              type="button"
              variant="default"
              size="icon"
              className="ml-auto size-7 rounded-full"
              style={{
                backgroundColor: "var(--accent-color)",
                color: "var(--accent-foreground)",
              }}
              aria-label="Stop generating"
            />
          }
        >
          <SquareIcon className="size-3.5 fill-current" />
        </ComposerPrimitive.Cancel>
      </AuiIf>
    </div>
  );
}

function UserMessage() {
  return (
    <MessagePrimitive.Root
      className="fade-in slide-in-from-bottom-1 animate-in mx-auto grid w-full max-w-[var(--thread-max-width)] auto-rows-auto grid-cols-[minmax(72px,1fr)_auto] content-start gap-y-2 px-2 duration-150"
      data-role="user"
    >
      <UserMessageAttachments />
      <div className="col-start-2 flex justify-end">
        <div className="flex size-8 shrink-0 items-center justify-center rounded-full bg-(--aui-user-avatar)">
          <UserIcon className="size-4" />
        </div>
      </div>

      <div className="relative col-start-2 min-w-0">
        <div className="text-foreground rounded-[var(--composer-radius)] bg-(--aui-user-message) px-4 py-2 break-words">
          <MessagePrimitive.Parts />
        </div>
        <div className="absolute top-1/2 left-0 -translate-x-full -translate-y-1/2 pr-2">
          <UserActionBar />
        </div>
      </div>

      <BranchPicker className="col-span-full col-start-1 -mr-1 justify-end" />
    </MessagePrimitive.Root>
  );
}

function UserActionBar() {
  const linearHistory = useContext(LinearHistory);
  if (linearHistory) return null;
  return (
    <ActionBarPrimitive.Root
      hideWhenRunning
      autohide="not-last"
      className="flex flex-col items-end"
    >
      <ActionBarPrimitive.Edit
        render={<TooltipIconButton tooltip="Edit" className="p-4" />}
      >
        <PencilIcon />
      </ActionBarPrimitive.Edit>
    </ActionBarPrimitive.Root>
  );
}

function EditComposer() {
  return (
    <MessagePrimitive.Root className="mx-auto flex w-full max-w-[var(--thread-max-width)] flex-col px-2">
      <ComposerPrimitive.Root className="ms-auto flex w-full max-w-[85%] cursor-text flex-col rounded-[var(--composer-radius)] border border-(--aui-border) bg-[var(--composer-bg)] transition-[border-color]">
        <ComposerPrimitive.Input
          className="text-foreground min-h-14 w-full resize-none bg-transparent px-4 pt-3 pb-1 text-base outline-none"
          autoFocus
        />
        <div className="mx-2.5 mb-2.5 flex items-center gap-1.5 self-end">
          <ComposerPrimitive.Cancel
            render={<Button variant="ghost" size="sm" className="h-8 px-3" />}
          >
            Cancel
          </ComposerPrimitive.Cancel>
          <ComposerPrimitive.Send
            render={<Button size="sm" className="h-8 px-3" />}
          >
            Update
          </ComposerPrimitive.Send>
        </div>
      </ComposerPrimitive.Root>
    </MessagePrimitive.Root>
  );
}

function AssistantMessage() {
  return (
    <MessagePrimitive.Root
      className="fade-in slide-in-from-bottom-1 animate-in relative mx-auto w-full max-w-[var(--thread-max-width)] px-2 duration-150"
      data-role="assistant"
    >
      <div className="flex gap-3">
        <div className="flex size-8 shrink-0 items-center justify-center rounded-full bg-(--aui-assistant-avatar)">
          <BotIcon className="size-4" />
        </div>
        <div className="min-w-0 flex-1">
          <div className="text-foreground leading-relaxed break-words">
            <MessagePrimitive.Parts
              components={{
                Text: AnswerMarkdown,
                tools: { Fallback: ToolFallback },
              }}
            />
            <MessageError />
            <MessageGraphLink />
            <AuiIf
              condition={(s) =>
                s.thread.isRunning && s.message.content.length === 0
              }
            >
              <div className="text-muted-foreground flex items-center gap-2">
                <LoaderIcon className="size-4 animate-spin" />
                <span className="text-sm">{"Thinking..."}</span>
              </div>
            </AuiIf>
          </div>

          <div className="mt-1 ml-2 flex min-h-6 items-center">
            <BranchPicker />
            <AssistantActionBar />
          </div>
        </div>
      </div>
    </MessagePrimitive.Root>
  );
}

function CitationLink({ href, children }: ComponentProps<"a">) {
  const onViewGraph = useContext(ViewGraph);
  const threadId = useAuiState((s) => s.threads.mainThreadId);
  const messageId = useAuiState((s) => s.message.id);
  const raw = useAuiState((s) => s.message.metadata.custom?.graph);
  const metadata = useAuiState((s) => s.message.metadata.custom?.metadata);
  const graph = useMemo(() => parseQueryGraph(raw), [raw]);
  const citation = href ? resolveCitation(graph, metadata, href) : undefined;
  const badge =
    "bg-muted text-muted-foreground hover:text-foreground mx-0.5 inline-flex cursor-pointer items-center rounded-md border px-1.5 text-xs font-medium whitespace-nowrap";
  if (citation && onViewGraph && threadId) {
    return (
      <button
        type="button"
        className={badge}
        title={citation.item.title}
        aria-controls="detail-panel"
        onClick={() => onViewGraph(threadId, messageId, citation.item.id)}
      >
        {citation.label}
      </button>
    );
  }
  const url = evidenceUrl(href);
  return url ? (
    <a className={badge} href={url} target="_blank" rel="noopener noreferrer">
      {new URL(url).hostname.replace(/^www\./, "")}
    </a>
  ) : (
    <span>{children}</span>
  );
}

const citationComponents = { a: CitationLink };

function AnswerMarkdown() {
  return <MarkdownText components={citationComponents} />;
}

function MessageGraphLink() {
  const onViewGraph = useContext(ViewGraph);
  const message = useAuiState((s) => s.message);
  const threadId = useAuiState((s) => s.threads.mainThreadId);
  const graph = parseQueryGraph(message.metadata.custom?.graph);
  if (!onViewGraph || !threadId || !graph?.nodes.length) return null;
  return (
    <button
      type="button"
      className="text-muted-foreground hover:text-foreground mt-2 block cursor-pointer text-sm underline underline-offset-4"
      onClick={() => onViewGraph(threadId, message.id)}
      aria-controls="detail-panel"
    >
      Xem đồ thị đã truy vấn
    </button>
  );
}

function MessageError() {
  return (
    <MessagePrimitive.Error>
      <ErrorPrimitive.Root className="border-destructive bg-destructive/10 text-destructive dark:bg-destructive/5 mt-2 rounded-md border p-3 text-sm dark:text-red-200">
        <ErrorPrimitive.Message className="line-clamp-2" />
      </ErrorPrimitive.Root>
    </MessagePrimitive.Error>
  );
}

function AssistantActionBar() {
  const linearHistory = useContext(LinearHistory);
  return (
    <ActionBarPrimitive.Root
      hideWhenRunning
      autohide="not-last"
      className="text-muted-foreground -ml-1 flex gap-1"
    >
      <ActionBarPrimitive.Copy render={<TooltipIconButton tooltip="Copy" />}>
        <AuiIf condition={(s) => s.message.isCopied}>
          <CheckIcon />
        </AuiIf>
        <AuiIf condition={(s) => !s.message.isCopied}>
          <CopyIcon />
        </AuiIf>
      </ActionBarPrimitive.Copy>
      <ActionBarPrimitive.ExportMarkdown
        render={<TooltipIconButton tooltip="Export as Markdown" />}
      >
        <DownloadIcon />
      </ActionBarPrimitive.ExportMarkdown>
      <AuiIf
        condition={(s) =>
          !linearHistory || s.message.status?.type === "incomplete"
        }
      >
        <ActionBarPrimitive.Reload
          render={
            <TooltipIconButton
              tooltip={linearHistory ? "Thử lại" : "Refresh"}
            />
          }
        >
          <RefreshCwIcon />
        </ActionBarPrimitive.Reload>
      </AuiIf>

      <ActionBarPrimitive.FeedbackPositive
        render={<TooltipIconButton tooltip="Good response" />}
      >
        <ThumbsUpIcon />
      </ActionBarPrimitive.FeedbackPositive>
      <ActionBarPrimitive.FeedbackNegative
        render={<TooltipIconButton tooltip="Bad response" />}
      >
        <ThumbsDownIcon />
      </ActionBarPrimitive.FeedbackNegative>
    </ActionBarPrimitive.Root>
  );
}

function BranchPicker({ className, ...rest }: { className?: string }) {
  const linearHistory = useContext(LinearHistory);
  if (linearHistory) return null;
  return (
    <BranchPickerPrimitive.Root
      hideWhenSingleBranch
      className={cn(
        "text-muted-foreground mr-2 -ml-2 inline-flex items-center text-xs",
        className,
      )}
      {...rest}
    >
      <BranchPickerPrimitive.Previous
        render={<TooltipIconButton tooltip="Previous" />}
      >
        <ChevronLeftIcon />
      </BranchPickerPrimitive.Previous>
      <span className="font-medium">
        <BranchPickerPrimitive.Number /> / <BranchPickerPrimitive.Count />
      </span>
      <BranchPickerPrimitive.Next render={<TooltipIconButton tooltip="Next" />}>
        <ChevronRightIcon />
      </BranchPickerPrimitive.Next>
    </BranchPickerPrimitive.Root>
  );
}
