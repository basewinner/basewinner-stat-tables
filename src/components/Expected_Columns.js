import { format } from 'date-fns'
import { basic }from './sortTypes'


export const EXPECTED_COLUMNS = [
  {
    Header: 'Team',
    Footer: 'Team',
    accessor: 'Team',   
  },
  {
    Header: 'Division',
    Footer: 'Division',
    accessor: 'Division',
  },

  {
    Header: 'W',
    Footer: 'W',
    accessor: 'W',
    disableFilters: true,
  },
  {
    Header: 'L',
    Footer: 'L',
    accessor: 'L',
    disableFilters: true,
  },
  {
    Footer: 'PCT',
    Header: 'PCT',
    accessor: 'PCT',
    disableFilters: true,
    sortType: basic,
    Cell: ({ value }) => {
      return format(value, value.toFixed(3))
    }
  },
  {
    Header: 'WRC+',
    Footer: 'WRC+',
    accessor: 'WRC+',
    disableFilters: true,
  },
  {
    Header: 'xFIP-',
    Footer: 'xFIP-',
    accessor: 'xFIP-',
    disableFilters: true,
  },
  {
    Header: 'DRS',
    Footer: 'DRS',
    accessor: 'DRS',
    disableFilters: true,
    Cell: ({ value }) => {
      return format(value, value.toFixed(0))
    }
  },
  {
    Header: 'xWins',
    Footer: 'xWins',
    accessor: 'xWins',
    disableFilters: true,
    Cell: ({ value }) => {
      return format(value, value.toFixed(1))
    }
  },
  {
    Header: 'xLoss',
    Footer: 'xLoss',
    accessor: 'xLoss',
    disableFilters: true,
    Cell: ({ value }) => {
      return format(value, value.toFixed(1))
    }
  },
  {
    Header: 'xPCT',
    Footer: 'xPCT',
    accessor: 'Implied PCt',
    disableFilters: true,
    sortType: basic,
    Cell: ({ value }) => {
      return (format(value, value.toFixed(3)))
    }
  },
  {
    Header: 'xW +-',
    Footer: 'xW +-',
    accessor: 'Xwins +-',
    disableFilters: true,
    sortType: basic,
    Cell: ({ value }) => {
      return format(value, value.toFixed(1))
    }
  },
]

