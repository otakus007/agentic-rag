import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import MessageBubble from '../MessageBubble.vue'

describe('MessageBubble', () => {
  it('renders user message with correct alignment', () => {
    const wrapper = mount(MessageBubble, {
      props: { message: { role: 'user', content: 'Hello' } },
    })
    expect(wrapper.text()).toContain('Hello')
    expect(wrapper.text()).toContain('You')
  })

  it('renders assistant message', () => {
    const wrapper = mount(MessageBubble, {
      props: { message: { role: 'assistant', content: 'Hi there!', sources: [] } },
    })
    expect(wrapper.text()).toContain('Hi there!')
    expect(wrapper.text()).toContain('Assistant')
  })

  it('renders citation markers as clickable elements', () => {
    const wrapper = mount(MessageBubble, {
      props: {
        message: { role: 'assistant', content: 'Based on [1] and [2], yes.', sources: [] },
      },
    })
    const html = wrapper.html()
    expect(html).toContain('data-cite="1"')
    expect(html).toContain('data-cite="2"')
  })
})
