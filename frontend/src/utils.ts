import { tzDate, parse, isAfter } from '@formkit/tempo'

export function sleep(ms: number) {
  return new Promise((resolve) => setTimeout(resolve, ms))
}

export function toLocal(time: string) {
  const localTz = Intl.DateTimeFormat().resolvedOptions().timeZone
  const parsedTime = parse(time, 'HH:mm:ssZ')
  return tzDate(parsedTime, localTz)
}

export function shiftType(start: Date) {
  return isAfter(start, parse('14:00:00+02:00', 'HH:mm:ssZ')) ? 'tarde' : 'mañana'
}
