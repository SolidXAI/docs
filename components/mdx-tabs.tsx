'use client';

import { Children, isValidElement, type ReactElement, type ReactNode } from 'react';
import { Tabs as FumaTabs, Tab as FumaTab } from 'fumadocs-ui/components/tabs';

type TabItemProps = {
  value: string;
  label: string;
  children?: ReactNode;
};

type TabsProps = {
  children?: ReactNode;
  defaultValue?: string;
};

type TabDefinition = {
  value: string;
  label: string;
  content: ReactNode;
};

export function TabItem(_props: TabItemProps) {
  return null;
}

function getTabs(children: ReactNode): TabDefinition[] {
  const tabs: TabDefinition[] = [];

  function walk(node: ReactNode) {
    Children.forEach(node, (child) => {
      if (!isValidElement(child)) return;

      const element = child as ReactElement<Partial<TabItemProps>>;
      const props = element.props;

      if (typeof props.label === 'string' && typeof props.value === 'string') {
        tabs.push({
          value: props.value,
          label: props.label,
          content: props.children,
        });
        return;
      }

      if (props.children) {
        walk(props.children);
      }
    });
  }

  walk(children);
  return tabs;
}

export function Tabs({ children, defaultValue }: TabsProps) {
  const tabs = getTabs(children);

  if (tabs.length === 0) return <>{children}</>;

  const defaultIndex = defaultValue
    ? Math.max(
        0,
        tabs.findIndex((tab) => tab.value === defaultValue),
      )
    : 0;

  return (
    <FumaTabs items={tabs.map((tab) => tab.label)} defaultIndex={defaultIndex}>
      {tabs.map((tab) => (
        <FumaTab key={tab.value}>{tab.content}</FumaTab>
      ))}
    </FumaTabs>
  );
}
